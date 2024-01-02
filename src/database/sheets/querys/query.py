import json

class Querys:
    def __init__(self, sheets_connector):
        self.sheets_connector = sheets_connector

    def cadastrar_aluno(self, aluno):
        # Lógica para cadastrar aluno na planilha usando sheets_connector
        data_aluno = {
            "Nome": aluno.nome,
            "Idade": aluno.idade,
            "Sexo": aluno.sexo,
            "Peso": aluno.peso,
            # Adicione outros campos conforme necessário
        }
        response_aluno = self.sheets_connector.post_data(json.dumps(data_aluno))
        return response_aluno

    def cadastrar_exercicio(self, exercicio):
        # Lógica para cadastrar exercício na planilha usando sheets_connector
        data_exercicio = {
            "TipoTreino": exercicio.tipoTreino,
            "Exercicio": exercicio.exercicio,
            "Serie": exercicio.serie,
            "Repeticao": exercicio.repeticao,
            "Descanso": exercicio.descanso,
            "Carga": exercicio.carga,
            "AlunoId": exercicio.aluno_id,
        }
        response_exercicio = self.sheets_connector.post_data(json.dumps(data_exercicio))
        return response_exercicio