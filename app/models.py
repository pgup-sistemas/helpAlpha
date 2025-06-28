from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash
    
    @staticmethod
    def get(user_id):
        # Simulação de banco de dados - em produção usar SQLAlchemy
        users = {
            '1': User('1', 'admin', generate_password_hash('admin123'))
        }
        return users.get(str(user_id))
    
    @staticmethod
    def authenticate(username, password):
        # Simulação de autenticação - em produção usar banco de dados
        users = {
            'admin': User('1', 'admin', generate_password_hash('admin123'))
        }
        user = users.get(username)
        if user and check_password_hash(user.password_hash, password):
            return user
        return None
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password) 