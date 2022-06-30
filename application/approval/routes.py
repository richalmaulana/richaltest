from flask import request, render_template, make_response, request, jsonify, session, redirect, url_for, send_from_directory, Blueprint, flash
from flask_login import current_user, login_required
from datetime import date
import json, requests, hashlib
import os
from application import app
from application.dbdvd import *

approval = Blueprint('approval', __name__)


@approval.route("/approval", methods=['GET'])
@login_required
def list_approval():
    '''Controller Home '''
    dataListSewa = getDataListSewa()
    print(dataListSewa)

    return render_template('approval/index.html', title='List Sewa', dataListSewa=dataListSewa['result'])


@approval.route("/approval/detail_approval", methods=['GET'])
@login_required
def detail_approval():

    no_id_sewa  = request.args['n']
    # print(no_id_sewa)

    dataDetailSewa = getDetailSewa(no_id_sewa)
    print(dataDetailSewa)

    return render_template('approval/detail_approval.html', title='Detail Persetujuan Sewa', dataDetailSewa = dataDetailSewa['result'])

@approval.route("/approval/setuju", methods=['POST'])
@login_required
def approval_setuju():

    today = date.today()
    tgl_app = today
    id_app = current_user.id
    no_id_sewa = request.form.get('sewa_id', None)

    print(no_id_sewa)


    # response = simpan_history_pengajuan()
    response = update_detail_pengajuan(id_app, tgl_app, no_id_sewa)

@approval.route("/approval/tolak", methods=['POST'])
@login_required
def approval_tolak():

    today = date.today()
    tgl_app = today
    id_app = current_user.id
    no_id_sewa = request.form.get('sewa_id', None)
    no_id_film = request.form.get('no_id_film', None)

    print(no_id_sewa)


    # response = simpan_history_pengajuan()

    jml_stock = getStock(no_id_film)
    data_jml_stock = jml_stock['result'][0]['dtl_stock']
    # print(data_jml_stock,type(data_jml_stock))
    stock = '1'
    tambah_stock = int(data_jml_stock) + int(stock) 
    # print(kurang_stock)
    response = update_stock(tambah_stock, no_id_film)
    response = update_detail_pengajuan_tolak(id_app, tgl_app, no_id_sewa)

  


    return response



    

	
