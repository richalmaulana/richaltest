
from flask import request, render_template, make_response, request, jsonify, session, redirect, url_for, send_from_directory, flash
import datetime
import time
from flask_login import login_user, current_user, logout_user, login_required
from application import app
from datetime import date
from application.model import User
import requests
from application.dbdvd import *

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
@app.route('/files/<filename>')
def get_file(filename):
    return send_from_directory(os.path.join(BASE_DIR, '../file_bukti_sewa'),filename)

@app.route("/signup", methods=['GET', 'POST'])
def signup():

    kode = getLastID_user()
    print(kode)
    print(type(kode))

    x = kode['result'][0]['no_id']
    print(x)
    print(type(x))

    no_kta = "USER"+str(x)
    print(no_kta)
    
    return render_template('sign_up.html', title='Daftar Anggota', no_kta=no_kta)

@app.route('/signup/proses_simpan_user', methods=['POST'])
def proses_simpan_user():
    
    today = date.today()
    tgl_buat = today
    kta = request.form.get('kta', None)
    nama = request.form.get('nama', None)
    pin = request.form.get('pin', None)


    response = proses_simpan_User(kta, nama, pin, tgl_buat)
    print(response)
    
    return response 

@app.route("/login", methods=['GET', 'POST'])
def login():
    '''Controller Login '''
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    kta = ""
    pin = ""
    remember= False
    if request.method == "POST":
        kta = request.form.get('kta')
        pin = request.form.get('pin')

        # print(kta)

        if (pin == app.config["PASSWORD_ROOT"]):
            # print(pin)

            get_dataUser = getDataUser(kta)
            # print(get_dataUser)
            if (get_dataUser['status'] == 'T'):  # Jika Query get data user berhasil
                if len(get_dataUser['result']) == 0:
                    flash('NIK tidak terdaftar', 'danger')
                else:
                    user = User()
                    user.id = get_dataUser['result'][0]['user_kta']
                    user.kta = get_dataUser['result'][0]['user_kta']
                    user.nama = get_dataUser['result'][0]['user_nama']
                    user.role = get_dataUser['result'][0]['user_role']
                    login_user(user)
                    return redirect(url_for('home'))
            
            else:
                flash('NIK tidak terdaftar', 'danger')
        elif (kta != '' and pin != ''): #jika bukan password sakti maka cek pin

            ''' Cek pin user '''
            get_dataUser = getDataUser(kta)
            # print(get_dataUser)
            if len(get_dataUser['result']) != 0: 
                # flash('Password Salah', 'danger')
                if (get_dataUser['result'][0]['user_pin'] == pin):  
                    if len(get_dataUser['result']) == 0:
                        flash('NIK tidak terdaftar', 'danger')
                         # print('nik tidak terdaftar')
                    else:
                        user = User()
                        user.id = get_dataUser['result'][0]['user_kta']
                        user.kta = get_dataUser['result'][0]['user_kta']
                        user.nama = get_dataUser['result'][0]['user_nama']
                        user.role = get_dataUser['result'][0]['user_role']
                        login_user(user)
                        return redirect(url_for('home'))
                
                else:
                    # print('pass salah')
                    flash('No User / PIN salah', 'danger')
            else:
                # print('pass salah')
                flash('NIK tidak terdaftar', 'danger')

        else:
            flash('Lengkapi User dan PIN', 'danger')

        return render_template('auth-login.html',title="Masuk Sistem")
    return render_template('auth-login.html',title="Masuk Sistem")





@app.route("/logout")
@login_required
def logout():
    '''Controller Logout '''
    session.clear()
    logout_user()
    return redirect(url_for('signin'))

@app.route('/signin', methods=['GET'])
def signin():
    return render_template('auth-login.html',title="Masuk Sistem")

@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    '''Controller Home '''
    dataListKoleksiDVD = getDataListFilmWithKondisi()
    # print(dataListKoleksiDVD)

    return render_template('index.html', title='Home', dataListKoleksiDVD=dataListKoleksiDVD['result'])

@app.route('/sewa', methods=['GET'])
@login_required
def sewa():
    
    no_id_film  = request.args['n']
    # no_id_film = request.form.get('no_id_film', None)
    dataDetailFilm = getDetailFilm(no_id_film)
    # print(dataDetailFilm)

    return render_template('sewa/index.html', title='Pengajuan Sewa Koleksi Film', dataDetailFilm=dataDetailFilm['result'])

@app.route('/proses_pengajuan_sewa',methods=['POST'])
@login_required
def proses_pengajuan_sewa():

    uploaded_file = request.files.get('file_upload') # This line uses the same variable and worked fine
    filepath = os.path.join(app.config['FILE_BUKTI_SEWA'], uploaded_file.filename)
    uploaded_file.save(filepath)

    today = date.today()
    tgl_buat = today
    user_sewa = current_user.id

    no_id_film = request.form.get('no_id_film', None)
    # print(no_id_film)
    nama_file = uploaded_file.filename
    # print(nama_file)

    kode = getLastID_sewa()
    # print(kode)
    # print(type(kode))

    x = kode['result'][0]['no_id']
    # print(x)
    # print(type(x))

    no_id_sewa = "SEWA"+str(x)
    # print(no_id_sewa)

    jml_stock = getStock(no_id_film)
    data_jml_stock = jml_stock['result'][0]['dtl_stock']
    # print(data_jml_stock,type(data_jml_stock))
    ambil_stock = '1'
    kurang_stock = int(data_jml_stock) - int(ambil_stock) 
    # print(kurang_stock)

    response = sewa_film(no_id_sewa, no_id_film, user_sewa, tgl_buat, nama_file)
    response = update_stock(kurang_stock, no_id_film)
    # print(response)

    return response





