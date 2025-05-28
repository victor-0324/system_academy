from datetime import datetime, timedelta
from flask import Flask, current_app

from apscheduler.schedulers.background import BackgroundScheduler
from src.database.models import ProgressoSemanal, HistoricoSemanal 


# Função que roda toda segunda-feira à 00:00 e move dados antigos para histórico
def resetar_progresso_semanal():
    agora = datetime.now()
    inicio_semana = (agora - timedelta(days=agora.weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    # Busca registros anteriores ao início da semana atual
    registros_antigos = (
        current_app.query(ProgressoSemanal)
        .filter(ProgressoSemanal.data_criacao < inicio_semana)
        .all()
    )

    if not registros_antigos:
        print("Nenhum registro antigo para resetar.")
        return

    print(f"Movendo {len(registros_antigos)} registros para histórico...")
    for r in registros_antigos:
        # Cria uma entrada no histórico
        historico = HistoricoSemanal(
            aluno_id=r.aluno_id,
            data_criacao=r.data_criacao,
            tempo_treino=r.tempo_treino,
            pontos=r.pontos,
        )
        current_app.add(historico)
        # Remove o registro original
        current_app.delete(r)

    current_app.commit()
    print("Reset semanal concluído e histórico atualizado.")

# Inicializa o scheduler no app Flask
def iniciar_scheduler(app: Flask):
    scheduler = BackgroundScheduler(timezone="America/Fortaleza")
    scheduler.add_job(
        func=resetar_progresso_semanal,
        trigger='cron',
        day_of_week='mon',
        hour=0,
        minute=0,
        id='reset_progresso_semanal'
    )
    scheduler.start()
    print("Scheduler iniciado: reset semanal agendado para toda segunda-feira 00:00.")
