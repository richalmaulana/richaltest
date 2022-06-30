from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)
app.config.from_pyfile('settings.py') #konfigurasi app diambil dari file settings.py
db = SQLAlchemy(app) #jika mengggunakan SQLAlchemy (ORM)
# csrf = CsrfProtect(app)

#konfigurasi login manager
app.jinja_env.add_extension('jinja2.ext.do')
csrf = CSRFProtect()

# csrf.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'signin'
login_manager.login_message_category = 'info'

#setiap tambah file controller di Folder Controller WAJIB di tambahkan juga disini
from application import routes
from application.upload.routes import upload
from application.approval.routes import approval
from application.report.routes import report
from application.history.routes import history

app.register_blueprint(upload)
app.register_blueprint(approval)
app.register_blueprint(report)
app.register_blueprint(history)