from typing import List
from src.database.models import Aluno, ExerciciosAluno
from werkzeug.security import check_password_hash, generate_password_hash
from src.database.config import db_connector, DBConnectionHandler
from sqlalchemy.orm import joinedload, load_only
from datetime import datetime

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

    def get_exercicios_by_aluno(self, aluno_id):
        exercicios = (
        self.session.query(ExerciciosAluno)
        .filter(ExerciciosAluno.aluno_id == aluno_id)
        .all()
        )
        return exercicios

    def verificar_credenciais(self, login, senha):
        aluno = (
            self.session.query(Aluno)
            .filter_by(login=login, senha=senha)  
            .first()
        )

        if aluno:
            return aluno, aluno.permissao

        return None, None

    def cadastrar_aluno(self, nome, idade, sexo, peso, ombro, torax, braco_d, braco_e, ant_d, ant_e, cintura, abdome, quadril, coxa_d, coxa_e, pant_d, pant_e, observacao, telefone, login, senha, data_entrada, data_pagamento, jatreino, permissao, exercicios):
        data_entrada = datetime.strptime(data_entrada, '%Y-%m-%d') if data_entrada else None
        data_pagamento = datetime.strptime(data_pagamento, '%Y-%m-%d') if data_pagamento else None

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
   
    def atualizar_dados(self, aluno_id, peso, ombro, torax, braco_d, braco_e, ant_d, ant_e, cintura, abdome, quadril, coxa_d, coxa_e, pant_d, pant_e, observacao, telefone, login, data_pagamento, senha, exercicios):
        aluno = self.session.query(Aluno).options(joinedload(Aluno.exercicios)).filter_by(id=aluno_id).first()
        historico_antes = aluno.medidas_historico()

        if aluno:
            aluno_antes = Aluno()
            aluno_antes.__dict__.update(aluno.__dict__)
            aluno_antes.medidas_antes = historico_antes[:-1]
            print(exercicios)
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
                aluno.observacao = observacao
                aluno.telefone = telefone
                aluno.login = login
                aluno.data_pagamento = datetime.strptime(data_pagamento, '%d/%m/%Y') if data_pagamento else None
                aluno.senha = senha
                aluno.data_atualizacao = datetime.utcnow()

                print(exercicios)
                if exercicios:
                    aluno.exercicios.clear()
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

