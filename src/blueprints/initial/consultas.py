from datetime import datetime, timedelta
from flask import json


def carregar_manifesto():
    """Carrega o arquivo manifest.json."""
    with open('src/static/manifest.json', 'r') as file:
        return json.load(file)

def calcular_proxima_data_pagamento(data_pagamento_atual):
    if data_pagamento_atual:
        # Converter a string da data de pagamento atual para um objeto datetime
        data_pagamento_atual = datetime.strptime(data_pagamento_atual, '%Y-%m-%d')
        # Calcular a próxima data de pagamento com base em 30 dias
        proxima_data_pagamento = data_pagamento_atual + timedelta(days=30)
        return proxima_data_pagamento.strftime('%d/%m/%Y')
    return None

def calcular_proxima_atualizacao(data_pagamento_atual):
    if data_pagamento_atual:
        # Converter a string da data de pagamento atual para um objeto datetime
        data_pagamento_atual = datetime.strptime(data_pagamento_atual, '%Y-%m-%d')
        # Calcular a próxima atualização com base em 60 dias
        proxima_atualizacao = data_pagamento_atual + timedelta(days=60)
        return proxima_atualizacao.strftime('%d/%m/%Y')
    return None

def verificar_atualizacao_exercicios(aluno, exercicios, inadimplente):
    """
    Verifica a necessidade de atualização dos exercícios de um aluno.
    
    Args:
    - aluno: Objeto aluno contendo id e nome.
    - exercicios: Lista de exercícios do aluno.
    - inadimplente: Booleano indicando se o aluno está inadimplente.

    Returns:
    - Um dicionário com informações sobre o exercício atrasado mais antigo ou uma mensagem.
    """
    exercicios_atrasados = []

    if exercicios:
        # Itera sobre os exercícios para verificar quais estão atrasados
        for exercicio in exercicios:
            if exercicio.atualizacao:
                # Calcula se a data de atualização está atrasada (60 dias atrás)
                data_limite_atualizacao = exercicio.atualizacao + timedelta(days=60)
                if datetime.now() > data_limite_atualizacao:
                    exercicio.em_atraso = True
                    exercicios_atrasados.append(exercicio)
                else:
                    exercicio.em_atraso = False
            else:
                exercicio.em_atraso = False

        # Se houver exercícios atrasados e o aluno não estiver inadimplente
        if exercicios_atrasados and not inadimplente:
            # Encontrando o exercício mais atrasado (com a data de atualização mais antiga)
            exercicio_mais_atrasado = min(exercicios_atrasados, key=lambda e: e.atualizacao)
            data_limite_atualizacao = exercicio_mais_atrasado.atualizacao + timedelta(days=60)
            
            return {
                'id': aluno.id,
                'nome': aluno.nome,
                'exercicio_atrasado': {
                    'atualizacao': exercicio_mais_atrasado.atualizacao.strftime('%d/%m/%Y'),
                    'dataLimiteAtualizacao': data_limite_atualizacao.strftime('%d/%m/%Y'),
                }
            }
    
    # Caso não haja exercícios atrasados
    return None

def obter_dados_alunos(alunos):
    """
    Processa uma lista de alunos para verificar status de pagamentos, atualizações e inadimplência.
    
    Args:
    - alunos: Lista de objetos contendo informações dos alunos.

    Returns:
    - Um dicionário contendo agrupamentos de alunos conforme seu status.
    """
    alunos_pagam_semana = []
    inadimplentes = []
    alunos_atualizar_exercicios = []
    total_alunos_ativos = 0

    for aluno in alunos:
        # Obtém informações de pagamento
        data_pagamento_atual = aluno.data_pagamento.strftime('%Y-%m-%d') if aluno.data_pagamento else None
        proxima_data_pagamento = calcular_proxima_data_pagamento(data_pagamento_atual)
        inadimplente = aluno.inadimplente
        exercicios = aluno.exercicios  

        # Verificar se o aluno está inadimplente
        if not inadimplente:
            total_alunos_ativos += 1
        else:
            inadimplentes.append({
                'id': aluno.id,
                'nome': aluno.nome,
                'dataPagamento': aluno.data_pagamento
            })

        # Filtrar alunos para pagamento nesta semana
        if proxima_data_pagamento and verificar_pagamento_proximo(proxima_data_pagamento, inadimplente):
            alunos_pagam_semana.append({
                'id': aluno.id,
                'nome': aluno.nome,
                'proximaDataPagamento': proxima_data_pagamento
            })

        # Verificar necessidade de atualização de exercícios
        atualizar_exercicio = verificar_atualizacao_exercicios(aluno, exercicios, inadimplente)
        if atualizar_exercicio:
            alunos_atualizar_exercicios.append(atualizar_exercicio)

    return {
        "total_alunos_ativos": total_alunos_ativos,
        "alunos_pagam_semana": alunos_pagam_semana,
        "inadimplentes": inadimplentes,
        "alunos_atualizar_exercicios": alunos_atualizar_exercicios
    }

def verificar_pagamento_proximo(proxima_data_pagamento, inadimplente):
    """Verifica se o pagamento está dentro dos próximos 6 dias e se o aluno não é inadimplente."""
    proxima_data_pagamento_dt = datetime.strptime(proxima_data_pagamento, '%d/%m/%Y')
    data_limite = datetime.now() + timedelta(days=6)
    return proxima_data_pagamento_dt <= data_limite and not inadimplente

def extrair_data_medidas(medidas):
    """Extrai e retorna a data mais recente de atualização de medidas."""
    datas_atualizacao = [medida.data_atualizacao for medida in medidas if medida.data_atualizacao]
    return max(datas_atualizacao) if datas_atualizacao else None

def verificar_necessidade_atualizacao(datas_medidas, inadimplente):
    """Verifica se as medidas precisam ser atualizadas nos próximos 6 dias."""
    if not datas_medidas:
        return True
    data_limite_atualizacao = datas_medidas + timedelta(days=60)
    data_limite_seis_dias = datetime.now() + timedelta(days=6)
    return datetime.now() <= data_limite_atualizacao <= data_limite_seis_dias and not inadimplente
