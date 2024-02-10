# pylint: disable=no-value-for-parameter,unused-variable
"""Rotas de Dashboard"""

from datetime import datetime
import json
from flask import Blueprint, request, render_template, url_for, redirect, jsonify, current_app
from src.database.querys import Querys 

from flask.views import MethodView



class ExerciciosView(MethodView):
    """CRUD dos Exercicios"""
    def get(self):
        """Envia as Transações de um projeto."""
        pass

    def post(self):
        """Cadastrar um exercicio no aluno"""
        data_json = request.get_json()
        alunoid = data_json['alunoId']
        tipotreino = data_json['tipoTreino']
        exercicio = data_json['exercicio']
        serie = data_json['serie']
        repeticao = data_json['repeticao']
        descanso = data_json['descanso']
        carga = data_json['carga']

        session = current_app.db.session
            # Crie uma instância da classe Querys
        querys_instance = Querys(session)

        querys_instance.cadastrar_ex(
                 alunoid, tipotreino, exercicio, serie, repeticao, descanso, carga
                )
        return jsonify({'success': True}), 200

    def put(self):
        """Edita uma transação"""
       

        return jsonify({"data": {}}), 200
    
    def delete(self, _id):
        """Deleta um Exercicio"""
        with current_app.app_context():
            session = current_app.db.session
            querys_instance = Querys(session)
            querys_instance.deletar_exercicio(_id)
            
        return jsonify({'success': True}), 200