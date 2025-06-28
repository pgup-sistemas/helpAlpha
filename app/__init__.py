from flask import Flask
from flask_login import LoginManager
from config import Config

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'admin_login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'warning'
    
    # User loader para Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.get(user_id)
    
    # Registrar as rotas públicas
    from app.routes import register_routes
    register_routes(app)
    
    # Registrar rotas administrativas
    from app.admin_routes import admin_login, admin_logout, admin_dashboard, admin_exames, admin_add_exame, admin_edit_exame, admin_delete_exame, admin_upload_excel, admin_download_template
    
    # Rotas administrativas
    app.add_url_rule('/admin/login', 'admin_login', admin_login, methods=['GET', 'POST'])
    app.add_url_rule('/admin/logout', 'admin_logout', admin_logout, methods=['GET'])
    app.add_url_rule('/admin', 'admin_dashboard', admin_dashboard, methods=['GET'])
    app.add_url_rule('/admin/exames', 'admin_exames', admin_exames, methods=['GET'])
    app.add_url_rule('/admin/exames/add', 'admin_add_exame', admin_add_exame, methods=['GET', 'POST'])
    app.add_url_rule('/admin/exames/edit/<nome>', 'admin_edit_exame', admin_edit_exame, methods=['GET', 'POST'])
    app.add_url_rule('/admin/exames/delete/<nome>', 'admin_delete_exame', admin_delete_exame, methods=['POST'])
    app.add_url_rule('/admin/upload-excel', 'admin_upload_excel', admin_upload_excel, methods=['GET', 'POST'])
    app.add_url_rule('/admin/download-template', 'admin_download_template', admin_download_template, methods=['GET'])
    
    return app 