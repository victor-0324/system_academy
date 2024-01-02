from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, user_id, aluno):
        self.id = user_id
        self.aluno = aluno

    @property
    def permissao(self):
        return self.aluno.get('Permissao', None)

    @property
    def inadimplente(self):
        # Adicione lógica para verificar inadimplência (se necessário)
        return False  # Altere conforme necessário

    @property
    def is_active(self):
        # Implemente a lógica para verificar se o usuário está ativo ou não
        return True

    @property
    def is_authenticated(self):
        # Implemente a lógica para verificar se o usuário está autenticado ou não
        return True

    @property
    def is_anonymous(self):
        # Implemente a lógica para verificar se o usuário é anônimo ou não
        return False
