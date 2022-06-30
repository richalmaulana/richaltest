from flask_login import UserMixin
from application import db, login_manager
from application.dbdvd import *

@login_manager.user_loader

def load_user(user_id): #fungsi ini selalu di load saat refresh page
    ''' Query lagi dari database buat check benar tidak user login nya '''
    get_data_user = getDataUser(user_id)
    print(get_data_user)
    user = User()
    if (get_data_user['status'] == 'T'):
        user.id = get_data_user['result'][0]['user_kta']
        user.kta = get_data_user['result'][0]['user_kta']
        user.nama = get_data_user['result'][0]['user_nama']
        user.role = get_data_user['result'][0]['user_role']

    return user

class User(db.Model, UserMixin): # class Session User Login
    id = db.Column(db.String(10), primary_key=True)