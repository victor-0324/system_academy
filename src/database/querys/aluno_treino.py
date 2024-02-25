from typing import List
from src.database.models import Aluno, ExerciciosAluno
from werkzeug.security import check_password_hash, generate_password_hash
from src.database.config import db_connector, DBConnectionHandler
from sqlalchemy.orm import joinedload, load_only
from datetime import datetime, timedelta
from flask import jsonify

class Querys():
   
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
        return (
            self.session.query(Aluno)
            .options(joinedload(Aluno.exercicios))  # Carregamento da relação exercicios
            .filter_by(id=aluno_id)
            .first()
        )
    
    def deletar(self, aluno_id):
    
        # Restante do código...
        aluno = (
            self.session.query(Aluno)
            .options(joinedload(Aluno.exercicios))
            .filter_by(id=aluno_id)
            .first()
        )

        if aluno:
            self.session.query(ExerciciosAluno).filter_by(aluno_id=aluno.id).delete()
            self.session.delete(aluno)
            self.session.commit()

            return True
        else:
            return False

    def buscar_exercicios_por_nome(self, nome_aluno):
        aluno = (
            self.session.query(Aluno)
            .filter(Aluno.nome == nome_aluno)
            .first()
        )

        if aluno:
           
            return aluno
        else:
            return None

    def get_exercicios_by_aluno(self, aluno_id):
        exercicios = (
        self.session.query(ExerciciosAluno)
        .filter(ExerciciosAluno.aluno_id == aluno_id)
        .all()
        )
        return exercicios

    def deletar_exercicio(self, exercicio_id):
        try:
            # Obtém o exercício pelo seu id
            exercicio = (
                self.session.query(ExerciciosAluno)
                .filter_by(id=exercicio_id)
                .first()
            )

            if exercicio:
                # Exclui o exercício diretamente do banco de dados
                self.session.delete(exercicio)
                self.session.commit()

                return True

            else:
                return False  # O exercício não foi encontrado

        except Exception as e:
            print(f'Erro ao excluir exercício: {str(e)}')
            return False

    def editar_exercicio(self, exercicio_id, novos_dados):
        try:
            # Obtém o exercício pelo seu id
            exercicio = (
                self.session.query(ExerciciosAluno)
                .filter_by(id=exercicio_id)
                .first()
            )
            print(exercicio)
            if exercicio:
               
                exercicio.tipoTreino = novos_dados.get('tipoTreino', exercicio.tipoTreino)
                exercicio.exercicio = novos_dados.get('exercicio', exercicio.exercicio)
                exercicio.serie = novos_dados.get('serie', exercicio.serie)
                exercicio.repeticao = novos_dados.get('repeticao', exercicio.repeticao)
                exercicio.descanso = novos_dados.get('descanso', exercicio.descanso)
                exercicio.carga = novos_dados.get('carga', exercicio.carga)

                # Commit para salvar as alterações no banco de dados
                self.session.commit()

                return {'mensagem': 'Exercício editado com sucesso', 'status_code': 200}

            else:
                return {'mensagem': 'Exercício não encontrado', 'status_code': 404}

        except Exception as e:
            print(f'Erro ao editar exercício: {str(e)}')
            return {'mensagem': 'Erro ao editar exercício. Consulte os logs para mais informações.', 'status_code': 500}
            
    def verificar_credenciais(self, login, senha):
        aluno = (
            self.session.query(Aluno)
            .filter_by(login=login, senha=senha)  
            .first()
        )

        if aluno:
            return aluno, aluno.permissao

        return None, None

    def cadastrar_ex(self, alunoid, tipotreino, exercicio, serie, repeticao, descanso, carga):
        exercicio = ExerciciosAluno(
            aluno_id=alunoid, tipoTreino=tipotreino, exercicio=exercicio, serie=serie, repeticao=repeticao, descanso=descanso,
            carga=carga
        )

        self.session.add(exercicio)
        self.session.commit()
        return exercicio

    def cadastrar_aluno(self, nome, idade, sexo, peso, ombro, torax, braco_d, braco_e, ant_d, ant_e, cintura, abdome, quadril, coxa_d, coxa_e, pant_d, pant_e, observacao, telefone, login, senha, data_entrada, data_pagamento, jatreino, permissao, exercicios):
        data_entrada = datetime.strptime(data_entrada, '%Y-%m-%d') if data_entrada else None
        data_pagamento = datetime.strptime(data_pagamento, '%Y-%m-%d') if data_pagamento else None

        # Configurando a data de pagamento para a data de entrada
        if data_pagamento is None:
            data_pagamento = data_entrada

        aluno = Aluno(
            nome=nome, idade=idade, sexo=sexo, peso=peso,
            ombro=ombro,torax=torax, braco_d=braco_d, braco_e=braco_e, ant_d=ant_d, ant_e=ant_e,cintura=cintura,
            abdome=abdome, quadril=quadril, coxa_d=coxa_d, coxa_e=coxa_e, pant_d=pant_d, pant_e=pant_e,
            observacao=observacao, telefone=telefone, login=login, senha=senha,
            data_entrada=data_entrada,
            data_pagamento=data_pagamento,
            jatreino=jatreino, permissao=permissao
        )
     # Adiciona o aluno ao histórico antes de fazer o commit
        historico_antes = aluno.medidas_historico()
        aluno.historico_medidas_peso = self._converter_datas_para_string(historico_antes)
        
        self.session.add(aluno)

        for exercicio in exercicios:
            exercicio_aluno = ExerciciosAluno(
                tipoTreino=exercicio.get('tipoTreino', ''),
                exercicio=exercicio.get('exercicio', ''),
                serie=exercicio.get('serie', ''),
                repeticao=exercicio.get('repeticao', ''),
                descanso=exercicio.get('descanso', ''),
                carga=exercicio.get('carga', '')
            )
            aluno.exercicios.append(exercicio_aluno)
        self.session.commit()
        return aluno
        
    def atualizar_medidas(self, aluno_id, peso, ombro, torax, braco_d, braco_e, ant_d, ant_e, cintura, abdome, quadril, coxa_d, coxa_e, pant_d, pant_e):
        aluno = self.session.query(Aluno).options(joinedload(Aluno.exercicios)).filter_by(id=aluno_id).first()
        historico_antes = aluno.medidas_historico()

        if aluno:
            aluno_antes = Aluno()
            aluno_antes.__dict__.update(aluno.__dict__)
            aluno_antes.medidas_antes = historico_antes[:-1]
          
            # Restringir a atualização apenas para medidas válidas
            if peso is not None and ombro is not None:
                aluno.peso = peso
                aluno.ombro = ombro
                aluno.torax = torax
                aluno.braco_d = braco_d
                aluno.braco_e = braco_e
                aluno.ant_d = ant_d
                aluno.ant_e = ant_e
                aluno.cintura = cintura
                aluno.abdome = abdome
                aluno.quadril = quadril
                aluno.coxa_d = coxa_d
                aluno.coxa_e = coxa_e
                aluno.pant_d = pant_d
                aluno.pant_e = pant_e
                aluno.data_atualizacao = datetime.utcnow()

                historico_antes = aluno_antes.medidas_historico()
                historico_depois = aluno.medidas_historico()

                historico_antes_str = self._converter_datas_para_string(historico_antes)
                historico_depois_str = self._converter_datas_para_string(historico_depois)
                aluno.historico_medidas_peso = historico_antes_str
                self.session.commit()

                return historico_antes_str, historico_depois_str
            else:
                # Lógica para lidar com medidas inválidas
                return None, None
        else:
            # Lógica para lidar com o aluno não encontrado
            return None, None

    def _converter_datas_para_string(self, historico):
        historico_str = []
        for medida in historico:
            medida_str = {key: value.strftime('%Y-%m-%d') if isinstance(value, datetime) else value for key, value in medida.items()}
            historico_str.append(medida_str)
        return historico_str

    def verificar_falta_tres_dias(self, aluno_id):
        aluno = (
            self.session.query(Aluno)
            .filter_by(id=aluno_id)
            .first()
        )

        if aluno and aluno.data_pagamento:
            # Calcular a data de vencimento do próximo pagamento (30 dias após o último pagamento)
            data_pagamento_proximo = aluno.data_pagamento + timedelta(days=32)

            # Calcular a diferença de dias entre a data de vencimento e a data atual
            diferenca_dias = (data_pagamento_proximo - datetime.utcnow()).days
            
            if diferenca_dias == 2:
                return "Seu pagamento está próximo de vencer! Por favor, efetue o pagamento nos próximos 2 dias para continuar acessando os treinos."
            elif diferenca_dias == 1:
                return "Seu pagamento está prestes a vencer! Por favor, efetue o pagamento até amanhã para continuar acessando os treinos."
            elif diferenca_dias == 0:
                return "Seu pagamento  vence hoje! Efetue o pagamento e continue acessando os treinos."
            else:
                return None 
        return None

    def atualizar_exercicios(self, aluno_id, exercicios):
        try:
            aluno = self.session.query(Aluno).options(joinedload(Aluno.exercicios)).filter_by(id=aluno_id).first()

            # Limpa os exercícios existentes
            aluno.exercicios.clear()

            # Adiciona os novos exercícios
            for exercicio_info in exercicios:
                exercicio = ExerciciosAluno(
                    tipoTreino=exercicio_info['tipoTreino'],
                    exercicio=exercicio_info['exercicio'],
                    serie=exercicio_info['serie'],
                    repeticao=exercicio_info['repeticao'],
                    descanso=exercicio_info['descanso'],
                    carga=exercicio_info['carga']
                )
                aluno.exercicios.append(exercicio)

            # Commit fora do loop para melhor desempenho e lógica de transação
            self.session.commit()

            return True  

        except Exception as e:
            print(f'Erro ao atualizar exercícios: {str(e)}')
            self.session.rollback()  
            return False 
            
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
                'id': exercicio.id,  
                'tipoTreino': exercicio.tipoTreino,
                'exercicio': exercicio.exercicio,
                'serie': exercicio.serie,
                'repeticao': exercicio.repeticao,
                'descanso': exercicio.descanso,
                'carga': exercicio.carga
            }
            exercicios_formatados.append(exercicio_dict)

        return exercicios_formatados

        exercicios_list = []
        exercicios_str = exercicios_str.strip("[]")  # Remove colchetes do início e do fim
        exercicios_entries = exercicios_str.split(', ')
        
        for exercicio_entry in exercicios_entries:
            dados_exercicio = exercicio_entry.split(' ')
            exercicio_dict = {
                'dia': dados_exercicio[0],
                'exercicio': dados_exercicio[1],
                'serie': dados_exercicio[2],
                'repeticao': dados_exercicio[3],
                'descanso': dados_exercicio[4],
                'carga': dados_exercicio[5]
                # Adicione outros atributos conforme necessário
            }
            exercicios_list.append(exercicio_dict)

        return exercicios_list

    def atualizardados(self, aluno_id, nome, idade, observacao, telefone, login, senha, data_pagamento, permissao):
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
                aluno.data_pagamento = datetime.strptime(data_pagamento, '%d/%m/%Y') if data_pagamento else None
                aluno.permissao = permissao

                # Commit apenas a atualização do aluno
                self.session.commit()
                print(aluno)
                return jsonify({'success': True}), 200
            
            else:
                # Lógica para lidar com medidas inválidas
                return jsonify({'error': 'Dados inválidos'}), 400
        else:
            # Lógica para lidar com o aluno não encontrado
            return jsonify({'error': 'Aluno não encontrado'}), 404

