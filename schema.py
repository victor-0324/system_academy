from datetime import datetime, timedelta
from flask import Flask, current_app

from apscheduler.schedulers.background import BackgroundScheduler
from src.database.models import ProgressoSemanal, HistoricoSemanal


# Função que roda toda segunda-feira à 00:00 e move dados antigos para histórico
def resetar_progresso_semanal():
    # 1) Determina o início da semana atual (segunda 00:00)
    agora = datetime.now()
    inicio_semana = (agora - timedelta(days=agora.weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    # 2) Abre a sessão do SQLAlchemy
    session = current_app.db.session

    # 3) Busca registros anteriores ao início da semana
    registros_antigos = (
        session.query(ProgressoSemanal)
        .filter(ProgressoSemanal.data_criacao < inicio_semana)
        .all()
    )

    if not registros_antigos:
        current_app.logger.info("Nenhum registro antigo para resetar.")
        return

    current_app.logger.info(f"Movendo {len(registros_antigos)} registros para histórico...")

    # 4) Transfere cada registro para o histórico e remove o original
    for prog in registros_antigos:
        historico = HistoricoSemanal(
            aluno_id=prog.aluno_id,
            dia=prog.dia,
            data_criacao=prog.data_criacao,
            tempo_treino=prog.tempo_treino,
            pontos=prog.pontos,
        )
        session.add(historico)
        session.delete(prog)

    # 5) Confirma as alterações
    session.commit()
    current_app.logger.info("Reset semanal concluído e histórico atualizado.")

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
