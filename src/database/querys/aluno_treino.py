from typing import List
from src.database.models import (
    Aluno,
    ExerciciosAluno,
    Medida,
    Category,
    Exercise,
    ProgressoSemanal,
)
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from flask import jsonify
from sqlalchemy import func
from zoneinfo import ZoneInfo


class Querys:

    def __init__(self, session):
        if session:
            self.session = session
        else:
            self.session = None

    def init_app(self, app):
        self.session = db.session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.session.remove()

    def mostrar(self, session):
        return session.query(Aluno).all()

    def mostrar_detalhes(self, aluno_id):
        aluno = (
            self.session.query(Aluno)
            .options(
                joinedload(Aluno.exercicios),
                joinedload(Aluno.medidas),
            )
            .filter_by(id=aluno_id)
            .first()
        )

        if aluno:
            return aluno
        else:
            return None

    def verificar_credenciais(self, login, senha):
        aluno = self.session.query(Aluno).filter_by(login=login, senha=senha).first()

        if aluno:
            return aluno, aluno.permissao

        return None, None

    def _converter_datas_para_string(self, historico):
        historico_str = []
        for medida in historico:
            medida_str = {
                key: (
                    value.strftime("%Y-%m-%d") if isinstance(value, datetime) else value
                )
                for key, value in medida.items()
            }
            historico_str.append(medida_str)
        return historico_str

    def verificar_falta_tres_dias(self, aluno_id):
        aluno = self.session.query(Aluno).filter_by(id=aluno_id).first()

        if aluno and aluno.data_pagamento:

            # Calcular a data de vencimento do próximo pagamento (30 dias após o último pagamento)
            data_pagamento_proximo = aluno.data_pagamento + timedelta(days=30)

            # Calcular a diferença de dias entre a data de vencimento e a data atual
            diferenca_dias = (data_pagamento_proximo - datetime.utcnow()).days

            if diferenca_dias == -2:  # Se o pagamento vence hoje
                return "Seu pagamento vence hoje! Efetue o pagamento e continue acessando os treinos."
            else:
                return None
        return None

    def criar_objeto_exercicio(self, aluno_id):
        exercicios = (
            self.session.query(ExerciciosAluno)
            .filter(ExerciciosAluno.aluno_id == aluno_id)
            .all()
        )
        aluno = aluno_id
        exercicios_formatados = []
        for index, exercicio in enumerate(exercicios):
            exercicio_dict = {
                "id": exercicio.id,
                "tipoTreino": exercicio.tipoTreino,
                "exercicio": exercicio.exercicio,
                "serie": exercicio.serie,
                "repeticao": exercicio.repeticao,
                "descanso": exercicio.descanso,
                "carga": exercicio.carga,
            }
            exercicios_formatados.append(exercicio_dict)

        return exercicios_formatados

    # \\\\\\\\ /////////

    # Deletar objetos no sistema
    def deletar_exercicio(self, exercicio_id):
        try:
            # Obtém o exercício pelo seu id
            exercicio = (
                self.session.query(ExerciciosAluno).filter_by(id=exercicio_id).first()
            )

            if exercicio:
                # Exclui o exercício diretamente do banco de dados
                self.session.delete(exercicio)
                self.session.commit()

                return True

            else:
                return False  # O exercício não foi encontrado

        except Exception as e:
            print(f"Erro ao excluir exercício: {str(e)}")
            return False

    def deletar_exercicio_cat(self, exercicio_id):
        try:
            # Obtém o exercício pelo seu id
            exercicio = self.session.query(Exercise).filter_by(id=exercicio_id).first()

            if exercicio:
                # Exclui o exercício diretamente do banco de dados
                self.session.delete(exercicio)
                self.session.commit()

                return True

            else:
                return False  # O exercício não foi encontrado

        except Exception as e:
            print(f"Erro ao excluir exercício: {str(e)}")
            return False

    def deletar(self, aluno_id):

        # Restante do código...
        aluno = (
            self.session.query(Aluno)
            .options(joinedload(Aluno.exercicios))
            .options(joinedload(Aluno.medidas))
            .filter_by(id=aluno_id)
            .first()
        )

        if aluno:
            self.session.query(ExerciciosAluno).filter_by(aluno_id=aluno.id).delete()
            self.session.query(ExerciciosAluno).filter(
                ExerciciosAluno.aluno_id.is_(None)
            ).delete(synchronize_session=False)
            self.session.query(Medida).filter_by(aluno_id=aluno.id).delete()
            self.session.delete(aluno)
            self.session.commit()

            return True
        else:
            return False

    def deletar_categoria(self, categoria_id):
        try:
            # Obtém a categoria pelo seu id
            categoria = self.session.query(Category).filter_by(id=categoria_id).first()

            if categoria:
                # Exclui a categoria juntamente com todos os exercícios associados
                self.session.delete(categoria)
                self.session.commit()

                return True

            else:
                return False  # A categoria não foi encontrada

        except Exception as e:
            print(f"Erro ao excluir categoria: {str(e)}")
            self.session.rollback()  # Reverte a transação em caso de erro
            return False

    # Editar elementos no sistema
    def editar_exercicio_cat(self, exercicio_id, novos_dados):
        try:
            # Obtém o exercício pelo seu id
            exercicio = self.session.query(Exercise).filter_by(id=exercicio_id).first()

            if exercicio:
                # Atualiza os dados do exercício com base nos valores fornecidos
                exercicio.tipoTreino = novos_dados.get(
                    "tipoTreino", exercicio.tipoTreino
                )
                exercicio.exercicio = novos_dados.get("exercicio", exercicio.exercicio)
                exercicio.serie = novos_dados.get("serie", exercicio.serie)
                exercicio.repeticao = novos_dados.get("repeticao", exercicio.repeticao)
                exercicio.descanso = novos_dados.get("descanso", exercicio.descanso)
                exercicio.carga = novos_dados.get("carga", exercicio.carga)

                # Commit para salvar as alterações no banco de dados
                self.session.commit()

                return {"mensagem": "Exercício editado com sucesso", "status_code": 200}

            else:
                return {"mensagem": "Exercício não encontrado", "status_code": 404}

        except Exception as e:
            print(f"Erro ao editar exercício: {str(e)}")
            return {
                "mensagem": "Erro ao editar exercício. Consulte os logs para mais informações.",
                "status_code": 500,
            }

    def editar_exercicio(self, exercicio_id, novos_dados):
        try:
            # Obtém o exercício pelo seu id
            exercicio = (
                self.session.query(ExerciciosAluno).filter_by(id=exercicio_id).first()
            )
            aluno = exercicio.aluno_id
            if not aluno:
                return "Sem aluno"
            # Buscar o aluno pelo nome
            aluno = self.session.query(Aluno).filter(Aluno.id == aluno).first()
            # Atualiza a data de atualização do aluno junto com a da tabela medidas
            aluno.data_atualizacao = datetime.now()

            if exercicio:
                exercicio.tipoTreino = novos_dados.get(
                    "tipoTreino", exercicio.tipoTreino
                )
                exercicio.exercicio = novos_dados.get("exercicio", exercicio.exercicio)
                exercicio.serie = novos_dados.get("serie", exercicio.serie)
                exercicio.repeticao = novos_dados.get("repeticao", exercicio.repeticao)
                exercicio.descanso = novos_dados.get("descanso", exercicio.descanso)
                exercicio.carga = novos_dados.get("carga", exercicio.carga)

                # Commit para salvar as alterações no banco de dados
                self.session.commit()

                return {"mensagem": "Exercício editado com sucesso", "status_code": 200}

            else:
                return {"mensagem": "Exercício não encontrado", "status_code": 404}

        except Exception as e:
            print(f"Erro ao editar exercício: {str(e)}")
            return {
                "mensagem": "Erro ao editar exercício. Consulte os logs para mais informações.",
                "status_code": 500,
            }

    # Buscas No Sistema
    def get_exercicios_by_aluno(self, aluno_id):
        exercicios = (
            self.session.query(ExerciciosAluno)
            .filter(ExerciciosAluno.aluno_id == aluno_id)
            .all()
        )
        return exercicios

    def get_ultima_medida(self, aluno_id):
        return (
            self.session.query(Medida)
            .filter_by(aluno_id=aluno_id)
            .order_by(Medida.data_atualizacao.desc())
            .first()
        )

    def get_medidas_por_aluno(self, aluno_id):
        medidas = (
            self.session.query(Medida)
            .filter_by(aluno_id=aluno_id)
            .order_by(Medida.data_atualizacao.desc())
            .all()
        )
        return [
            {
                "peso": m.peso,
                "ombro": m.ombro,
                "torax": m.torax,
                "braco_d": m.braco_d,
                "braco_e": m.braco_e,
                "ant_d": m.ant_d,
                "ant_e": m.ant_e,
                "cintura": m.cintura,
                "abdome": m.abdome,
                "quadril": m.quadril,
                "coxa_d": m.coxa_d,
                "coxa_e": m.coxa_e,
                "pant_d": m.pant_d,
                "pant_e": m.pant_e,
                "data_atualizacao": m.data_atualizacao,
            }
            for m in medidas
        ]

    def buscar_exercicios_por_nome(self, nome_aluno, filtro_dias):
        try:
            # Busca o aluno pelo nome
            aluno = self.session.query(Aluno).filter(Aluno.nome == nome_aluno).first()

            if aluno:
                # Consulta os exercícios associados ao aluno
                query = self.session.query(ExerciciosAluno).filter(
                    ExerciciosAluno.aluno_id == aluno.id
                )

                # Aplica filtro baseado em filtro_dias, se necessário
                if filtro_dias and filtro_dias.lower() != "todos":
                    # print(f"Aplicando filtro de dias: {filtro_dias}")
                    query = query.filter(ExerciciosAluno.tipoTreino == filtro_dias)

                # Executa a consulta
                exercicios = query.all()

                # Cria uma lista de dicionários com os dados dos exercícios
                exercicios_data = [
                    {
                        "id": e.id,
                        "tipoTreino": e.tipoTreino,
                        "exercicio": e.exercicio,
                        "serie": e.serie,
                        "repeticao": e.repeticao,
                        "descanso": e.descanso,
                        "carga": e.carga,
                    }
                    for e in exercicios
                ]
                # print(exercicios_data)
                return exercicios_data
            else:
                print("Aluno não encontrado")
                return None
        except Exception as e:
            print(f"Erro ao buscar exercícios: {e}")
            return None

    def obter_categorias(self):
        try:
            # Query para buscar todas as categorias
            categorias = self.session.query(Category).all()
            return categorias
        except Exception as e:
            print(f"Erro ao buscar categorias: {e}")
            return []

    def obter_categoria_por_id(self, categoria_id):
        """
        Obtém o nome de uma categoria específica pelo seu ID.

        :param categoria_id: ID da categoria.
        :return: Nome da categoria como string, ou None se a categoria não for encontrada.
        """
        try:
            categoria = (
                self.session.query(Category).filter_by(id=categoria_id).one_or_none()
            )
            if categoria:
                return categoria.name  # Retorna o nome da categoria
            return None
        except Exception as e:
            print(f"Erro ao obter categoria com ID {categoria_id}: {e}")
            return None

    def obter_exercicios_por_categoria(self, categoria_id):
        """
        Obtém todos os exercícios associados a uma categoria específica.

        :param categoria_id: ID da categoria.
        :return: Lista de objetos Exercise.
        """
        try:
            return (
                self.session.query(Exercise).filter_by(category_id=categoria_id).all()
            )
        except Exception as e:
            print(f"Erro ao obter exercícios para a categoria {categoria_id}: {e}")
            return []

    # Atualizaçoes
    def atualizardados(
        self,
        aluno_id,
        nome,
        idade,
        observacao,
        telefone,
        login,
        senha,
        data_pagamento,
        permissao,
        pagamento,
    ):
        # Verificar se o aluno existe
        aluno = self.session.query(Aluno).filter_by(id=aluno_id).first()

        if aluno:
            # Restringir a atualização apenas para medidas válidas
            if nome is not None and idade is not None:
                # Atualizar os atributos diretamente no objeto existente
                aluno.nome = nome
                aluno.idade = idade
                aluno.observacao = observacao
                aluno.telefone = telefone
                aluno.login = login
                aluno.senha = senha
                aluno.data_pagamento = (
                    datetime.strptime(data_pagamento, "%d/%m/%Y")
                    if data_pagamento
                    else None
                )
                aluno.permissao = permissao
                aluno.pagamento = pagamento

                # Commit apenas a atualização do aluno
                self.session.commit()
                return jsonify({"success": True}), 200

            else:
                # Lógica para lidar com medidas inválidas
                return jsonify({"error": "Dados inválidos"}), 400
        else:
            # Lógica para lidar com o aluno não encontrado
            return jsonify({"error": "Aluno não encontrado"}), 404

    def atualizar_exercicios_filtry(self, aluno_id, exercicios_filtrados):
        try:
            # Buscar o aluno pelo ID
            aluno = self.session.query(Aluno).get(aluno_id)
            if not aluno:
                print("Aluno não encontrado")
                return False

            # Buscar exercícios atuais do aluno
            exercicios_atual = (
                self.session.query(ExerciciosAluno)
                .filter(ExerciciosAluno.aluno_id == aluno_id)
                .all()
            )

            # Criar um dicionário para armazenar exercícios filtrados por tipoTreino
            exercicios_filtrados_dict = {}
            for exercicio in exercicios_filtrados:
                tipoTreino = exercicio.get("tipoTreino")
                if tipoTreino not in exercicios_filtrados_dict:
                    exercicios_filtrados_dict[tipoTreino] = {}
                exercicios_filtrados_dict[tipoTreino][exercicio.get("id")] = exercicio

            # Criar um dicionário para armazenar os IDs de exercícios atuais por tipoTreino
            exercicios_atual_dict = {}
            for ex_atual in exercicios_atual:
                tipoTreino = ex_atual.tipoTreino
                if tipoTreino not in exercicios_atual_dict:
                    exercicios_atual_dict[tipoTreino] = {}
                exercicios_atual_dict[tipoTreino][ex_atual.id] = ex_atual

            # Adicionar ou atualizar exercícios filtrados
            for (
                tipoTreino,
                exercicios_filtrados_tipo,
            ) in exercicios_filtrados_dict.items():
                # Verificar se há exercícios atuais para este tipoTreino
                exercicios_atual_tipo = exercicios_atual_dict.get(tipoTreino, {})

                # Atualizar ou adicionar exercícios
                for ex_id, exercicio in exercicios_filtrados_tipo.items():

                    ex_atual = exercicios_atual_tipo.get(ex_id)
                    if ex_atual:
                        # Atualizar exercício existente
                        ex_atual.tipoTreino = exercicio.get("tipoTreino")
                        ex_atual.exercicio = exercicio.get("exercicio")
                        ex_atual.serie = exercicio.get("serie")
                        ex_atual.repeticao = exercicio.get("repeticao")
                        ex_atual.descanso = exercicio.get("descanso")
                        ex_atual.carga = exercicio.get("carga")
                    else:
                        # Adicionar novo exercício se não existir
                        novo_exercicio = ExerciciosAluno(
                            tipoTreino=exercicio.get("tipoTreino"),
                            exercicio=exercicio.get("exercicio"),
                            serie=exercicio.get("serie"),
                            repeticao=exercicio.get("repeticao"),
                            descanso=exercicio.get("descanso"),
                            carga=exercicio.get("carga"),
                            aluno_id=aluno_id,
                        )
                        self.session.add(novo_exercicio)

                # Remover exercícios antigos que não estão mais na lista filtrada
                for ex_id, ex_atual in exercicios_atual_tipo.items():
                    if ex_id not in exercicios_filtrados_tipo:
                        self.session.delete(ex_atual)

            # Commit das mudanças
            self.session.commit()
            return True

        except Exception as e:
            print(f"Erro ao atualizar exercícios: {e}")
            self.session.rollback()
            return False

    def atualizar_medidas(
        self,
        aluno_id,
        peso,
        ombro,
        torax,
        braco_d,
        braco_e,
        ant_d,
        ant_e,
        cintura,
        abdome,
        quadril,
        coxa_d,
        coxa_e,
        pant_d,
        pant_e,
    ):
        aluno = self.session.query(Aluno).filter_by(id=aluno_id).first()

        if aluno:
            # Cria uma nova instância de Medida com os dados fornecidos
            medida = Medida(
                aluno_id=aluno_id,
                peso=peso,
                ombro=ombro,
                torax=torax,
                braco_d=braco_d,
                braco_e=braco_e,
                ant_d=ant_d,
                ant_e=ant_e,
                cintura=cintura,
                abdome=abdome,
                quadril=quadril,
                coxa_d=coxa_d,
                coxa_e=coxa_e,
                pant_d=pant_d,
                pant_e=pant_e,
                data_atualizacao=datetime.now(),  # Atualiza a data_atualizacao de Medida
            )

            # Adiciona a nova medida à sessão
            self.session.add(medida)

            # Faz o commit da sessão, salvando as alterações no banco de dados
            self.session.commit()
        else:
            raise ValueError(f"Aluno com id {aluno_id} não encontrado")

    def atualizar_exercicios(self, aluno_id, exercicios):
        try:
            aluno = (
                self.session.query(Aluno)
                .options(joinedload(Aluno.exercicios))
                .filter_by(id=aluno_id)
                .first()
            )

            # Limpa os exercícios existentes
            aluno.exercicios.clear()
            # Atualiza a data de atualização do aluno junto com a da tabela medidas
            aluno.data_atualizacao = datetime.now()

            # Adiciona os novos exercícios
            for exercicio_info in exercicios:
                exercicio = ExerciciosAluno(
                    aluno_id=aluno_id,
                    tipoTreino=exercicio_info["tipoTreino"],
                    exercicio=exercicio_info["exercicio"],
                    serie=exercicio_info["serie"],
                    repeticao=exercicio_info["repeticao"],
                    descanso=exercicio_info["descanso"],
                    carga=exercicio_info["carga"],
                )
                aluno.exercicios.append(exercicio)

            # Commit fora do loop para melhor desempenho e lógica de transação
            self.session.commit()

            return True

        except Exception as e:
            print(f"Erro ao atualizar exercícios: {str(e)}")
            self.session.rollback()
            return False

    def atualizar_exercicios_cat(self, nome_aluno, filtro_dias, categoriaId):
        try:
            # Buscar o aluno pelo nome
            aluno = self.session.query(Aluno).filter(Aluno.nome == nome_aluno).first()
            if not aluno:
                print("Aluno não encontrado")
                return False
            # Atualiza a data de atualização do aluno junto com a da tabela medidas
            aluno.data_atualizacao = datetime.now()

            # Buscar os exercícios associados ao aluno
            query = self.session.query(ExerciciosAluno).filter(
                ExerciciosAluno.aluno_id == aluno.id
            )

            # Aplica o filtro baseado em filtro_dias
            if filtro_dias and filtro_dias.lower() != "todos":
                query = query.filter(ExerciciosAluno.tipoTreino == filtro_dias)

            exercicios_aluno = query.all()

            # Criar um dicionário para armazenar exercícios filtrados por ID
            exercicios_aluno_dict = {e.id: e for e in exercicios_aluno}

            # Buscar os exercícios atuais da categoria
            exercicios_categoria = (
                self.session.query(Exercise)
                .filter(Exercise.category_id == categoriaId)
                .all()
            )

            # Criar um dicionário para armazenar os exercícios da categoria por ID
            exercicios_categoria_dict = {e.id: e for e in exercicios_categoria}

            if filtro_dias.lower() == "todos":
                # Excluir todos os exercícios atuais da categoria
                for ex_atual in exercicios_categoria:
                    self.session.delete(ex_atual)

                # Adicionar todos os exercícios filtrados do aluno à categoria
                for exercicio in exercicios_aluno:
                    novo_exercicio = Exercise(
                        tipoTreino=exercicio.tipoTreino,
                        exercicio=exercicio.exercicio,
                        serie=exercicio.serie,
                        repeticao=exercicio.repeticao,
                        descanso=exercicio.descanso,
                        carga=exercicio.carga,
                        category_id=categoriaId,
                    )
                    self.session.add(novo_exercicio)
            else:
                # Remover apenas os exercícios da categoria que correspondem ao filtro
                for ex_atual in exercicios_categoria:
                    if ex_atual.tipoTreino == filtro_dias:
                        self.session.delete(ex_atual)

                # Adicionar ou atualizar exercícios da categoria conforme o filtro
                for ex_id, exercicio in exercicios_aluno_dict.items():
                    if ex_id in exercicios_categoria_dict:
                        # Atualizar exercício existente na categoria
                        ex_atual = exercicios_categoria_dict[ex_id]
                        ex_atual.tipoTreino = exercicio.tipoTreino
                        ex_atual.exercicio = exercicio.exercicio
                        ex_atual.serie = exercicio.serie
                        ex_atual.repeticao = exercicio.repeticao
                        ex_atual.descanso = exercicio.descanso
                        ex_atual.carga = exercicio.carga
                    else:
                        # Adicionar novo exercício à categoria
                        novo_exercicio = Exercise(
                            tipoTreino=exercicio.tipoTreino,
                            exercicio=exercicio.exercicio,
                            serie=exercicio.serie,
                            repeticao=exercicio.repeticao,
                            descanso=exercicio.descanso,
                            carga=exercicio.carga,
                            category_id=categoriaId,
                        )
                        self.session.add(novo_exercicio)

            # Commit das mudanças
            self.session.commit()
            return True

        except Exception as e:
            print(f"Erro ao atualizar exercícios: {e}")
            self.session.rollback()
            return False

    def atualizar_exercicios_aluno(self, nome_aluno, filtro_dias, categoriaId):
        try:
            # Buscar o aluno pelo nome
            aluno = self.session.query(Aluno).filter(Aluno.nome == nome_aluno).first()
            if not aluno:
                print("Aluno não encontrado")
                return False

            # Atualiza a data de atualização do aluno junto com a da tabela medidas
            aluno.data_atualizacao = datetime.now()

            # Buscar os exercícios da categoria selecionada
            exercicios_categoria = (
                self.session.query(Exercise)
                .filter(Exercise.category_id == categoriaId)
                .all()
            )

            if filtro_dias.lower() == "todos":
                # Deletar todos os exercícios do aluno
                self.session.query(ExerciciosAluno).filter(
                    ExerciciosAluno.aluno_id == aluno.id
                ).delete()

                # Adicionar todos os exercícios da categoria ao aluno
                for exercicio in exercicios_categoria:
                    novo_exercicio = ExerciciosAluno(
                        aluno_id=aluno.id,
                        tipoTreino=exercicio.tipoTreino,
                        exercicio=exercicio.exercicio,
                        serie=exercicio.serie,
                        repeticao=exercicio.repeticao,
                        descanso=exercicio.descanso,
                        carga=exercicio.carga,
                    )
                    self.session.add(novo_exercicio)
            else:
                # Deletar os exercícios do aluno que correspondem ao filtro
                self.session.query(ExerciciosAluno).filter(
                    ExerciciosAluno.aluno_id == aluno.id,
                    ExerciciosAluno.tipoTreino == filtro_dias,
                ).delete()

                # Adicionar novos exercícios da categoria conforme o filtro
                for exercicio in exercicios_categoria:
                    if exercicio.tipoTreino == filtro_dias:
                        novo_exercicio = ExerciciosAluno(
                            aluno_id=aluno.id,
                            tipoTreino=exercicio.tipoTreino,
                            exercicio=exercicio.exercicio,
                            serie=exercicio.serie,
                            repeticao=exercicio.repeticao,
                            descanso=exercicio.descanso,
                            carga=exercicio.carga,
                        )
                        self.session.add(novo_exercicio)

            # Commit das mudanças
            self.session.commit()
            return True

        except Exception as e:
            print(f"Erro ao atualizar exercícios: {e}")
            self.session.rollback()
            return False

    def limpar_alunos(self):
        # Define o limite de 3 meses atrás
        limite = datetime.now() - timedelta(days=90)

        # Busca os alunos que não pagam há mais de 3 meses
        alunos_inadimplentes = (
            self.session.query(Aluno).filter(Aluno.data_pagamento < limite).all()
        )

        # Exclui cada um deles
        for aluno in alunos_inadimplentes:
            self.session.delete(aluno)

        # Confirma as exclusões no banco
        self.session.commit()
        print(f"{len(alunos_inadimplentes)} aluno(s) excluído(s) por inadimplência.")
        return f"{len(alunos_inadimplentes)} aluno(s) excluído(s) por inadimplência."

    # Cadastramentos, adicionar
    def cadastrar_ex(
        self, alunoid, tipotreino, exercicio, serie, repeticao, descanso, carga
    ):
        aluno = self.session.query(Aluno).filter(Aluno.id == alunoid).first()

        # Atualiza a data de atualização do aluno junto com a da tabela medidas
        aluno.data_atualizacao = datetime.now()

        exercicio = ExerciciosAluno(
            aluno_id=alunoid,
            tipoTreino=tipotreino,
            exercicio=exercicio,
            serie=serie,
            repeticao=repeticao,
            descanso=descanso,
            carga=carga,
        )

        self.session.add(exercicio)
        self.session.commit()
        return exercicio

    def cadastrar_aluno(
        self,
        nome,
        idade,
        sexo,
        peso,
        ombro,
        torax,
        braco_d,
        braco_e,
        ant_d,
        ant_e,
        cintura,
        abdome,
        quadril,
        coxa_d,
        coxa_e,
        pant_d,
        pant_e,
        observacao,
        telefone,
        login,
        senha,
        data_entrada,
        data_pagamento,
        jatreino,
        permissao,
        exercicios,
    ):
        try:
            # Convertendo as datas para o formato correto
            data_entrada = (
                datetime.strptime(data_entrada, "%Y-%m-%d") if data_entrada else None
            )
            data_pagamento = (
                datetime.strptime(data_pagamento, "%Y-%m-%d")
                if data_pagamento
                else None
            )

            # Configurando a data de pagamento para a data de entrada, se necessário
            if data_pagamento is None:
                data_pagamento = data_entrada

            # Criando o objeto Aluno
            aluno = Aluno(
                nome=nome,
                idade=idade,
                sexo=sexo,
                observacao=observacao,
                telefone=telefone,
                login=login,
                senha=senha,
                data_entrada=datetime.now(),
                data_pagamento=data_pagamento,
                data_atualizacao=datetime.now(),
                jatreino=jatreino,
                permissao=permissao,
            )

            # Adicionando o aluno à sessão e comitando
            self.session.add(aluno)
            self.session.commit()

            # Recuperando o ID do aluno recém-criado
            aluno_id = aluno.id

            # Adicionando os exercícios do aluno
            for exercicio in exercicios:
                exercicio_aluno = ExerciciosAluno(
                    tipoTreino=exercicio.get("tipoTreino", ""),
                    exercicio=exercicio.get("exercicio", ""),
                    serie=exercicio.get("serie", ""),
                    repeticao=exercicio.get("repeticao", ""),
                    descanso=exercicio.get("descanso", ""),
                    carga=exercicio.get("carga", ""),
                    aluno_id=aluno_id,  # Associe o exercício ao aluno
                )
                self.session.add(exercicio_aluno)

            # Criando o objeto Medida associado ao aluno
            medida = Medida(
                aluno_id=aluno_id,
                peso=peso,
                ombro=ombro,
                torax=torax,
                braco_d=braco_d,
                braco_e=braco_e,
                ant_d=ant_d,
                ant_e=ant_e,
                cintura=cintura,
                abdome=abdome,
                quadril=quadril,
                coxa_d=coxa_d,
                coxa_e=coxa_e,
                data_atualizacao=datetime.now(),
                pant_d=pant_d,
                pant_e=pant_e,
            )

            # Adicionando a medida à sessão
            self.session.add(medida)

            # Comitando todas as alterações
            self.session.commit()

            return aluno

        except Exception as e:
            # Revertendo a sessão em caso de erro
            self.session.rollback()
            raise

    def adicionar_categoria_e_exercicios(self, categoria_nome, exercicios):
        try:
            # Verificar se a categoria já existe
            categoria = (
                self.session.query(Category).filter_by(name=categoria_nome).first()
            )
            if not categoria:
                # Se a categoria não existir, criar uma nova
                categoria = Category(name=categoria_nome)
                self.session.add(categoria)
                self.session.commit()  # Commit para garantir que o ID da categoria esteja disponível

            # Adicionar cada exercício à categoria
            for exercicio_data in exercicios:
                novo_exercicio = Exercise(
                    tipoTreino=exercicio_data.get("diasSemana", ""),
                    exercicio=exercicio_data.get(
                        "exercicio", ""
                    ),  # Usando o campo correto para o nome do exercício
                    serie=exercicio_data.get("serie", ""),
                    repeticao=exercicio_data.get("repeticao", ""),
                    descanso=exercicio_data.get("descanso", ""),
                    carga=exercicio_data.get("carga", ""),
                    category_id=categoria.id,
                )
                self.session.add(novo_exercicio)

            # Salvar as mudanças
            self.session.commit()
            return True

        except Exception as e:
            print(f"Erro ao adicionar categoria e exercícios: {str(e)}")
            self.session.rollback()  # Rollback em caso de erro
            return False

    def adicionar_exercicio(self, dados):
        try:
            # Itera sobre a lista de exercícios enviada
            for exercicio in dados.get("exercicios", []):
                novo_exercicio = Exercise(
                    tipoTreino=dados.get("diasSemana"),
                    exercicio=exercicio.get("nome"),
                    serie=exercicio.get("serie"),
                    repeticao=exercicio.get("repeticao"),
                    descanso=exercicio.get("descanso"),
                    carga=exercicio.get("carga"),
                    category_id=dados.get("categoria"),
                )
                self.session.add(novo_exercicio)

            self.session.commit()
            return True, "Exercícios adicionados com sucesso"

        except Exception as e:
            self.session.rollback()
            print(f"Erro ao adicionar exercício: {str(e)}")
            return False, "Erro ao adicionar exercícios"

    def busca_progresso_semanal(self, aluno_id):
        progresso = (
            self.session.query(ProgressoSemanal).filter_by(aluno_id=aluno_id).all()
        )
        return progresso

    def salvar_progresso(self, aluno_id, duracao, pontos):
        # 1) Mapeia weekday para pt-BR
        dias = [
            "segunda-feira",
            "terça-feira",
            "quarta-feira",
            "quinta-feira",
            "sexta-feira",
            "sábado",
            "domingo",
        ]

        fuso_brasilia = ZoneInfo("America/Sao_Paulo")
        # obtém o datetime “agora” já no timezone correto
        agora = datetime.now(fuso_brasilia)
        hoje_idx = agora.weekday()  # 0=segunda ... 6=domingo
        dia_pt = dias[hoje_idx]

        # 2) Não grava domingo
        if dia_pt == "domingo":
            return False

        # 3) Busca (ou não) o registro de hoje
        prog = (
            self.session.query(ProgressoSemanal)
            .filter_by(aluno_id=aluno_id, dia=dia_pt)
            .first()
        )

        if prog:
            # 3a) Acumula sempre o tempo
            prog.tempo_treino += duracao

            # 3b) Só atribui pontos se ainda não houve pontuação hoje
            if prog.pontos == 0:
                prog.pontos = pontos

            prog.data_criacao = datetime.now(fuso_brasilia)
        else:
            # 4) Primeiro treino do dia: cria registro com tempo+pontos
            prog = ProgressoSemanal(
                aluno_id=aluno_id,
                dia=dia_pt,
                tempo_treino=duracao,
                pontos=pontos,
                data_criacao=datetime.now(fuso_brasilia),
                finalizado=True,
            )
            self.session.add(prog)

        self.session.commit()
        return True

    def calcular_pontos(self, duracao: timedelta) -> int:
        MAX_DURACAO = timedelta(hours=2)
        PONTOS_MAX = 100
        PONTOS_MIN = 10
        if duracao >= MAX_DURACAO:
            return PONTOS_MAX
        elif duracao >= timedelta(minutes=30):
            return max(
                int(
                    (duracao.total_seconds() / MAX_DURACAO.total_seconds()) * PONTOS_MAX
                ),
                PONTOS_MIN,
            )
        else:
            return PONTOS_MIN


    def calcular_nivel(self, aluno_id) -> str:
        """
        Retorna o nível do aluno nesta semana:
        - Iniciante (<30 pts)
        - Intermediário (30–99 pts)
        - Avançado (>=100 pts)
        """
        # 1) Calcula intervalo segunda 00:00 até sábado 23:59:59
        fuso_brasilia = ZoneInfo("America/Sao_Paulo")
        agora = datetime.now(fuso_brasilia)
        inicio_semana = (agora - timedelta(days=agora.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        fim_semana = inicio_semana + timedelta(days=5, hours=23, minutes=59, seconds=59)

        # 2) Soma pontos desta semana (segunda–sábado)
        total = (
            self.session.query(func.coalesce(func.sum(ProgressoSemanal.pontos), 0))
            .filter(
                ProgressoSemanal.aluno_id == aluno_id,
                ProgressoSemanal.data_criacao >= inicio_semana,
                ProgressoSemanal.data_criacao <= fim_semana,
            )
            .scalar()
        )

        # 3) Define níveis
        if total < 30:
            return "Iniciante"
        elif total < 100:
            return "Intermediário"
        else:
            return "Avançado"


    def calcular_conquista(self, mapa: dict) -> str:
        """
        De segunda (0) a sábado (5):
        - total_dias: quantos dias tiveram ≥5min
        Retorna UMA mensagem, na prioridade:
        1) Semana completa 🔥 (6 dias)
        2) 3 Dias de Treino 🥇  (total_dias >= 3)
        3) X Dias de Treino 🎯  (1 <= total_dias < 3)
        4) 😴 Sem Treino      (total_dias == 0)
        """
        MIN_SEGUNDOS = 5 * 60
        fuso = ZoneInfo("America/Sao_Paulo")
        hoje = datetime.now(fuso)
        inicio_sem = (hoje - timedelta(days=hoje.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        # Datas de segunda (0) a sábado (5)
        dias = [(inicio_sem + timedelta(days=i)).date().isoformat() for i in range(6)]
        # Marca se treinou ≥5min em cada dia
        valido = [mapa.get(d, {}).get("tempo", 0) >= MIN_SEGUNDOS for d in dias]
        total_dias = sum(valido)

        # 1) Semana completa (6 dias)
        if total_dias == 6:
            return "💪🏼 SEMANA COMPLETA 🔥"

        # 2) Três ou mais dias (não precisa ser seguidos)
        if total_dias >= 3:
            return f"🥇 {total_dias} Dias de Treino"

        # 3) Um ou dois dias
        if total_dias >= 1:
            return f"🎯 {total_dias} Dias de Treino"

        # 4) Sem treino
        return "😴 Sem Treino"
