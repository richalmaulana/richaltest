from flask import request, render_template, make_response, request, jsonify, session, redirect, url_for, send_file, send_from_directory, Blueprint, flash, Response
from flask_login import current_user, login_required
from datetime import date
import json, requests, hashlib
import csv
import os
from application import app
from application.dbdvd import *

# from application.dbmatrat import (savetoko)

report = Blueprint('report', __name__)

@report.route('/report', methods=["GET"])
@login_required
def report_pengajuan():
    

    dataListFilm = getDataListFilm()
    print(dataListFilm)

    return render_template('report/index.html', title='Report Koleksi Film', dataListFilm=dataListFilm['result'])


@report.route('/report/hapus_film', methods=['POST'])
@login_required
def delete_film():

    # no_id_film = request.form.get('no_id', None)
    # no_id_film  = request.args['n']

    inp = request.form
    print(inp['no_id_film'])

    user_hapus = current_user.id
    today = date.today()
    tgl_update = today
    response = proses_hapus_film(user_hapus, tgl_update, inp['no_id_film'])
    print(response)


    return response

@report.route("/report/detail_update", methods=['GET'])
@login_required
def detail_update():

    no_id_film  = request.args['n']
    # print(no_id_film)

    dataDetailFilm = getDetailFilm(no_id_film)
    print(dataDetailFilm)

    return render_template('report/detail_update.html', title='Detail Update Film', dataDetailFilm = dataDetailFilm['result'])

@report.route("/report/proses_update_detail", methods=['POST'])
@login_required
def proses_update_detail():

    today = date.today()
    tgl_update = today
    user_update = current_user.id

    no_id_film = request.form.get('no_id_film', None)
    judul_film = request.form.get('judul_film', None)
    category = request.form.get('category', None)
    descp = request.form.get('descp', None)
    rating = request.form.get('rating', None)
    kualitas = request.form.get('kualitas', None)
    stock = request.form.get('stock', None)
    status = request.form.get('status', None)
    if(status == "Aktif"):
        flag = "T"
    elif(status == "Tidak Aktif"):
        flag = "F" 
    status_aktif = flag

    response = proses_update_film(judul_film, category, descp, rating, kualitas, stock, flag, user_update, tgl_update, no_id_film)
    print(response)


    return response
   


  
      










