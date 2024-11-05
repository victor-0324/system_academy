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

def verificar_atualizacao_medidas(aluno, medidas, inadimplente):
    if medidas:
        datas_atualizacao = [medida.data_atualizacao for medida in medidas if medida.data_atualizacao]
        datas_medidas = max(datas_atualizacao) if datas_atualizacao else None
    else:
        datas_medidas = None

    if datas_medidas:
        data_limite_atualizacao = datas_medidas + timedelta(days=60)
        data_limite_seis_dias = datetime.now() + timedelta(days=6)
        if datetime.now() <= data_limite_atualizacao <= data_limite_seis_dias and not inadimplente:
            return {
                'id': aluno.id,
                'nome': aluno.nome,
                'ultimaAtualizacaoMedidas': datas_medidas.strftime('%d/%m/%Y'),
                'dataLimiteAtualizacao': data_limite_atualizacao.strftime('%d/%m/%Y')
            }
    else:
        return {'id': aluno.id, 'nome': aluno.nome, 'mensagem': 'Sem Data De Atualização'}
    return None

def obter_dados_alunos(alunos):
    alunos_pagam_semana = []
    inadimplentes = []
    alunos_atualizar_medidas = []
    total_alunos_ativos = 0

    for aluno in alunos:
        data_pagamento_atual = aluno.data_pagamento.strftime('%Y-%m-%d') if aluno.data_pagamento else None
        proxima_data_pagamento = calcular_proxima_data_pagamento(data_pagamento_atual)
        inadimplente = aluno.inadimplente
        medidas = aluno.medidas

        # Verificar se o aluno está inadimplente
        if not inadimplente:
            total_alunos_ativos += 1
        else:
            inadimplentes.append({
                'id': aluno.id,
                'nome': aluno.nome,
                'dataPagamento': aluno.data_pagamento if aluno.data_pagamento else 'N/A'
            })

        # Filtrar alunos para pagamento nesta semana
        if proxima_data_pagamento and verificar_pagamento_proximo(proxima_data_pagamento, inadimplente):
            alunos_pagam_semana.append({
                'id': aluno.id,
                'nome': aluno.nome,
                'proximaDataPagamento': proxima_data_pagamento
            })

        # Verificar necessidade de atualização de medidas
        atualizar_medidas_info = verificar_atualizacao_medidas(aluno, medidas, inadimplente)
        if atualizar_medidas_info:
            alunos_atualizar_medidas.append(atualizar_medidas_info)

    return {
        "total_alunos_ativos": total_alunos_ativos,
        "alunos_pagam_semana": alunos_pagam_semana,
        "inadimplentes": inadimplentes,
        "alunos_atualizar_medidas": alunos_atualizar_medidas
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
