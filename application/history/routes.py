from flask import request, render_template, make_response, request, jsonify, session, redirect, url_for, send_from_directory, Blueprint, flash
from flask_login import current_user, login_required
from datetime import date
import json, requests, hashlib
import os
from application import app
from application.dbdvd import *

history = Blueprint('history', __name__)

@history.route("/history", methods=['GET'])
@login_required
def list_history():
    '''Controller Home '''

    id_user = current_user.id
    dataListSewa = getDataListSewaCUS(id_user)
    print(dataListSewa)

    return render_template('history/index.html', title='List Sewa', dataListSewa=dataListSewa['result'])


@history.route("/history/detail_pengembalian", methods=['GET'])
@login_required
def detail_history():

    no_id_sewa  = request.args['n']
    # print(no_id_sewa)

    dataDetailSewa = getDetailSewa(no_id_sewa)
    print(dataDetailSewa)

    return render_template('history/detail_pengembalian.html', title='Detail Pengembalian Sewa', dataDetailSewa = dataDetailSewa['result'])

@history.route("/history/pengembalian", methods=['POST'])
@login_required
def pengembalian():

    today = date.today()
    tgl_buat = today
    id_app = current_user.id
    no_id_sewa = request.form.get('sewa_id', None)
    no_id_film = request.form.get('sewa_id_dvd', None)
    feedback = request.form.get('feedback', None)
    rating = request.form.get('rating', None)

    print(no_id_sewa)

    kode = getLastID_history()
    # print(kode)
    # print(type(kode))

    x = kode['result'][0]['no_id']
    # print(x)
    # print(type(x))

    no_id_history = "HIS"+str(x)
    # print(no_id_sewa)

    jml_stock = getStock(no_id_film)
    data_jml_stock = jml_stock['result'][0]['dtl_stock']
    # print(data_jml_stock,type(data_jml_stock))
    stock = '1'
    tambah_stock = int(data_jml_stock) + int(stock) 
    # print(kurang_stock)

    response = insert_history(no_id_history, no_id_film, id_app, feedback, rating, tgl_buat, no_id_sewa)
    response = update_stock(tambah_stock, no_id_film)
    response = update_detail_pengembalian(id_app, tgl_buat, no_id_sewa)

  


    return response



    

	
