from flask import request, render_template, make_response, request, jsonify, session, redirect, url_for, send_from_directory, Blueprint, flash
from flask_login import current_user, login_required
from datetime import date
import json, requests, hashlib
import csv
import pandas as pd
import os
from application import app
from application.dbdvd import *

upload = Blueprint('upload', __name__)

@upload.route('/upload', methods=["GET", "POST"])
@login_required
def buat_pengajuan():
      
    return render_template('upload/index.html')
      


@upload.route('/upload/upload_dvd',methods=['POST'])
@login_required
def upload_dvd():
    res = {}

    uploaded_file = request.files.get('file_upload') # This line uses the same variable and worked fine
    # print('uploaded_file : ', uploaded_file)
    filepath = os.path.join(app.config['FILE_UPLOADS'], uploaded_file.filename)
    uploaded_file.save(filepath)


    data = []
    dataDVD = []
    data = pd.read_excel (filepath)
    tempData = list(data.values)

    for dt in tempData:
        # print(dt, len(dt))
        temp_dict = {}
        temp_dict['judul_film'] = dt[0]  
        temp_dict['category'] = dt[1] 
        temp_dict['rating'] = dt[2] 
        temp_dict['kualitas'] = dt[3] 
        temp_dict['descp'] = dt[4] 
        temp_dict['stock'] = dt[5] 


        dataDVD.append(temp_dict)

    res['result'] = dataDVD

    return res



@upload.route('/upload/proses_simpan',methods=['POST'])
@login_required
def proses_simpan():
    
    today = date.today()
    year = today.strftime('%m%y')  

    dataDVD = json.loads(request.form.get('dataUpload', []))

    user_buat = current_user.id  
    tgl_buat = today   

    for dt in dataDVD:
        kode = getLastID()
        print(kode)
        print(type(kode))

        x = kode['result'][0]['no_id']
        print(x)
        print(type(x))

        no_id_film = "DVD"+"-"+str(year)+"-"+str(x)
        print(no_id_film)
        response = upload_film(no_id_film, dt['judul_film'], dt['category'], dt['rating'], dt['kualitas'], dt['descp'], dt['stock'], user_buat, tgl_buat)
        print(response)
    
    return response

    

	
