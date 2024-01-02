"""Gerindo dados em uma planilha google sheets"""
import requests
import json
import uuid 
from datetime import datetime, timedelta

class SheetsConnector:
    """Conectando ao google sheets"""
    def __init__(self):
        """Conectando ao google sheets"""
                        
        self.base_url = "https://script.google.com/macros/s/AKfycbzBe7Il5DiBfMUY0XbrhX0pWqlgW6Yg_BmNBHBl8c0_Zv_964oPwzEKCCtgUbsA4aNtcg/exec"
                        

    def post_data(self, data_json: dict):
        try:
            url_sheet = self.base_url
            
            response = requests.post(
                url_sheet,
                headers={"Content-Type": "application/json"},
                data=data_json,
                timeout=10
            )

            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar dados para a folha: {e}")
            return None


    def get_data(self):
        try:
            url_sheet = f"{self.base_url}"
            response = requests.get(url_sheet, timeout=10)
            response.raise_for_status()
            alunos_data = response.json()
            print(f"Dados brutos da planilha: {alunos_data}")
            return response

        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter dados: {e}")
            return None

    def cadastrar_aluno(self, nome, idade, sexo, observacao, telefone, login, senha, data_entrada, data_pagamento, jatreino, permissao,  peso, ombro, torax, braco_d, braco_e, ant_d, ant_e, cintura, abdome, quadril, coxa_d, coxa_e, pant_d, pant_e, exercicios):

        # Lógica para cadastrar aluno na planilha usando sheets_connector
        id_aluno = str(uuid.uuid4())

        exercicios_data = json.dumps(exercicios)

        medidas = {
            "Data": datetime.utcnow().isoformat(),
            "Peso": peso,
            "Ombro": ombro,
            "Torax": torax,
            "Braco_d": braco_d,
            "Braco_e": braco_e,
            "Ant_d": ant_d,
            "Ant_e": ant_e,
            "Cintura": cintura,
            "Abdome": abdome,
            "Quadril": quadril,
            "Coxa_d": coxa_d,
            "Coxa_e": coxa_e,
            "Pant_d": pant_d,
            "Pant_e": pant_e,
        }
        medidas_json = json.dumps(medidas)

        data_aluno = {
            "Aluno_id": id_aluno,
            "Nome": nome,
            "Idade": idade,
            "Sexo": sexo,
            "Observacao": observacao,
            "Telefone": telefone,
            "Login": login,
            "Senha": senha,
            "Data_entrada": data_entrada,
            "Data_pagamento": data_pagamento,
            "Jatreino": jatreino,
            "Permissao": permissao,
            "Peso": peso,
            "Ombro": ombro,
            "Torax": torax,
            "Braco_d": braco_d,
            "Braco_e": braco_e,
            "Ant_d": ant_d,
            "Ant_e": ant_e,
            "Cintura": cintura,
            "Abdome": abdome,
            "Quadril": quadril,
            "Coxa_d": coxa_d,
            "Coxa_e": coxa_e,
            "Pant_d": pant_d,
            "Pant_e": pant_e,
            "Exercicios": exercicios_data,
            "Medidas": medidas_json
            }

        response_aluno = self.post_data(json.dumps(data_aluno))

        return response_aluno

   
        # Lógica para cadastrar aluno na planilha usando sheets_connector
        id_aluno = str(uuid.uuid4())

        medidas_data = json.dumps(medidas)
        data_aluno = {
           
            "Medidas": medidas_data
            }
        response_aluno = self.post_data(json.dumps(data_aluno))

        return response_aluno

        
    def get_aluno_por_login_senha(self, login, senha):
        try:
            # Utilize a rota de pesquisa da sua API, se disponível
            url_sheet = f"{self.base_url}?Login={login}&action=login"
            response = requests.get(url_sheet, timeout=10)
            response.raise_for_status()
            aluno_data = response.json()

            if aluno_data and 'status' in aluno_data and aluno_data['status'] == 'success':
                data = aluno_data.get('data', [])

                if len(data) > 0 and len(data[0]) > 5:
                    aluno_id = data[0]  
                    aluno = self.obter_aluno_por_id(aluno_id)
                    
                    if aluno and aluno["Login"] == login and str(aluno["Senha"]) == senha:
                        return aluno
                    else:
                        print("Aluno não encontrado ou dados de login/senha incorretos.")
                        return None
                else:
                    print("Dados de login e senha não encontrados na lista.")
                    return None
            else:
                print("Erro na requisição ou status não é 'success'.")
                return None

        except Exception as e:
            print(f"Erro na requisição: {e}")
            return None
    
    def get_aluno_por_nome(self, nome_aluno):
        try:
            # Utilize a rota de pesquisa da sua API, se disponível
            url_sheet = f"{self.base_url}?Nome={nome_aluno}"
            response = requests.get(url_sheet, timeout=10)
            response.raise_for_status()
            aluno_data = response.json()

            if 'status' in aluno_data and aluno_data['status'] == 'success':
                # Se houver mais de um aluno, encontre o aluno específico pelo nome
                alunos = aluno_data.get('data', [])
                for aluno in alunos:
                    if aluno.get('Nome') == nome_aluno:
                        exercicios_json = aluno.get('Exercicios', '[]')
                        exercicios = json.loads(exercicios_json)
                       
                        return exercicios
                       
                # Se nenhum aluno foi encontrado com o nome específico
                return None
            else:
                return None
        except Exception as e:
            print(f"Erro na requisição: {e}")
            return None

    def obter_todos_alunos(self):
        try:
            url_sheet = self.base_url
            response = requests.get(url_sheet, timeout=10)
            response.raise_for_status()
            alunos_data = response.json()

            if 'status' in alunos_data and alunos_data['status'] == 'success':
                
                alunos = alunos_data['data']
                for aluno in alunos:
                    # Converter as datas para objetos datetime
                    aluno['Data_entrada'] = self.converter_data(aluno.get('Data_entrada', ''))
                    aluno['Data_pagamento'] = self.converter_data(aluno.get('Data_pagamento', ''))
                    aluno['Data_atualizacao'] = self.converter_data(aluno.get('Data_atualizacao', ''))
                    aluno['Exercicios'] = json.loads(aluno.get('Exercicios', '[]'))

                return alunos
            else:
                return None

        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter todos os alunos: {e}")
            return None
            
    def converter_data(self, data_str):
        if isinstance(data_str, datetime):
            return data_str  # Se já for um datetime, retorna sem conversão
        elif isinstance(data_str, str):
            try:
                # Verifica se a data já está no formato correto
                datetime.strptime(data_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                return datetime.strptime(data_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            except ValueError:
                try:
                    # Verifica se a data já está no formato correto
                    datetime.strptime(data_str, '%d/%m/%Y')
                    return datetime.strptime(data_str, '%d/%m/%Y')
                except ValueError:
                    return None
        else:
            return None

    def calcular_inadimplencia(self, aluno):
        if aluno and aluno['Data_pagamento']:
            if isinstance(aluno['Data_pagamento'], str):
                # Se for uma string, converter para datetime
                data_pagamento_atual = datetime.strptime(aluno['Data_pagamento'], '%Y-%m-%dT%H:%M:%S.%fZ')
            else:
                # Se já for um datetime, usar diretamente
                data_pagamento_atual = aluno['Data_pagamento']

            prazo_pagamento = timedelta(days=30)
            
            # Calcular a data limite
            data_limite = data_pagamento_atual + prazo_pagamento

            return datetime.utcnow() > data_limite
        else:
            return True

    def obter_aluno_por_id(self, aluno_id):
        # Obter todos os alunos da planilha
        alunos = self.obter_todos_alunos()

        # Procurar o aluno com o ID fornecido
        for aluno in alunos:
            if aluno.get('Aluno_id') == aluno_id:
                return aluno
        return None 

    def deletar_aluno(self, aluno_id):
        """
        Deleta um aluno da planilha Google Sheets pelo ID.

        Args:
            aluno_id (str): O ID do aluno a ser deletado.

        Returns:
            requests.Response: A resposta da API do Google Sheets.
        """
        try:
            url_sheet = f"{self.base_url}?Aluno_id={aluno_id}&action=delete_row"
            response_aluno = requests.get(url_sheet, timeout=10)
            
            response_aluno.raise_for_status()
            return response_aluno
        except requests.exceptions.RequestException as e:
            print(f"Erro ao deletar aluno: {e}")
            return None

    def atualizar_aluno(self, aluno_id, peso, ombro, torax,
                    braco_d, braco_e, ant_d, ant_e,
                    cintura, abdome, quadril, coxa_d, coxa_e, pant_d, pant_e,
                    observacao, telefone, login, data_pagamento, senha, exercicios
                    ):

        aluno = self.obter_aluno_por_id(aluno_id)
        
        # Verifique se há exercícios existentes
        exercicios_existentes = aluno["Exercicios"]
        
        # Se exercicios não estiver vazio, mantenha os exercícios existentes
        if exercicios:
            # Adicione os novos exercícios à lista existente ou mantenha os existentes
            novo_exercicios =  exercicios
            aluno["Exercicios"] = json.dumps(novo_exercicios)
        else:
            # Se não houver novos exercícios, mantenha os existentes
            aluno["Exercicios"] = json.dumps(exercicios_existentes)



        aluno["Peso"] = peso
        aluno["Ombro"] = ombro
        aluno["Torax"] = torax
        aluno["Braco_d"] = braco_d
        aluno["Braco_e"] = braco_e
        aluno["Ant_d"] = ant_d
        aluno["Ant_e"] = ant_e
        aluno["Cintura"] = cintura
        aluno["Abdome"] = abdome
        aluno["Quadril"] = quadril
        aluno["Coxa_d"] = coxa_d
        aluno["Coxa_e"] = coxa_e
        aluno["Pant_d"] = pant_d
        aluno["Pant_e"] = pant_e
        aluno["Observacao"] = observacao
        aluno["Telefone"] = telefone
        aluno["Login"] = login
        aluno['Data_pagamento'] = data_pagamento
        aluno["Senha"] = senha
        

        # Adicione as medidas como um JSON com a nova data
        medidas = {
            "Data": datetime.utcnow().isoformat(),
            "Peso": peso,
            "Ombro": ombro,
            "Torax": torax,
            "Braco_d": braco_d,
            "Braco_e": braco_e,
            "Ant_d": ant_d,
            "Ant_e": ant_e,
            "Cintura": cintura,
            "Abdome": abdome,
            "Quadril": quadril,
            "Coxa_d": coxa_d,
            "Coxa_e": coxa_e,
            "Pant_d": pant_d,
            "Pant_e": pant_e,
        }

        medidas_json = json.dumps(medidas)
        

        if 'Medidas' in aluno:
            medidas_anteriores = json.loads(aluno['Medidas'])
            if not isinstance(medidas_anteriores, list):
                medidas_anteriores = [medidas_anteriores]

            medidas_anteriores.append(medidas)
            aluno['Medidas'] = json.dumps(medidas_anteriores)
        else:
            aluno['Medidas'] = json.dumps([medidas])

        

        # Converta os campos do tipo datetime
        self.convert_datetime_fields(aluno)

        response_aluno = self.post_data(json.dumps(aluno))

        return response_aluno

    def convert_datetime_fields(self, aluno): 

        aluno['Data_entrada'] = aluno['Data_entrada'].isoformat()
        return aluno 

    def verificar_falta_tres_dias(self, aluno):
        
        data_pagamento = aluno["Data_pagamento"]
        

        if aluno and data_pagamento:
            # Calcular a data de vencimento do próximo pagamento (30 dias após o último pagamento)
            data_pagamento_proximo = data_pagamento + timedelta(days=31)

            # Calcular a diferença de dias entre a data de vencimento e a data atual
            diferenca_dias = (data_pagamento_proximo - datetime.utcnow()).days
            
            if diferenca_dias == 3:
                return "Seu pagamento está próximo de vencer! Por favor, efetue o pagamento nos próximos 3 dias para continuar acessando os treinos."
            elif diferenca_dias == 2:
                return "Seu pagamento está próximo de vencer! Por favor, efetue o pagamento nos próximos 2 dias para continuar acessando os treinos."
            elif diferenca_dias == 1:
                return "Seu pagamento vence hoje! Efetue o pagamento e continue acessando os treinos."
            else:
                return None
        return "Erro"
