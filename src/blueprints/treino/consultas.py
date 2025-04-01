# from src.database.models import Aluno, ExerciciosAluno, Medida, Category, Exercise, ProgressoSemanal
# from src.database.querys import Querys
# from datetime import timedelta
# from flask import current_app



# class ConsultaTreino: 

#     def busca_progresso_semanal(self, aluno_id):
#         return Querys.session(ProgressoSemanal).filter_by(aluno_id=aluno_id).all()
    

#     def salvar_progresso(self, aluno_id, inicio_treino, duracao, pontos):
#         session = current_app.db.session
#         # Crie uma instância da classe Querys
#         querys_instance = Querys(session)
#         progresso = ProgressoSemanal(
#             aluno_id=aluno_id,
#             dia=inicio_treino.strftime("%A"),  # Nome do dia da semana
#             tempo_treino=duracao,
#             pontos=pontos
#         )
#         querys_instance.add(progresso)
#         current_app.commit()  # Confirma a inserção no banco
    

#     def calcular_pontos(self, duracao: timedelta) -> int:
#         MAX_DURACAO = timedelta(hours=2) 
#         PONTOS_MAX = 100
#         PONTOS_MIN = 10 
#         if duracao >= MAX_DURACAO:
#             return PONTOS_MAX
#         elif duracao >= timedelta(minutes=30):
#             return max(int((duracao.total_seconds() / MAX_DURACAO.total_seconds()) * PONTOS_MAX), PONTOS_MIN)
#         else:
#             return PONTOS_MIN
        
