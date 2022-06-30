import psycopg2
import json
import os
import requests, datetime
from werkzeug.utils import secure_filename
from application import app
from application.queryFile import QueryStringDb
from application.static.format import rows_to_dict, rows_to_dict_list
from application.static.respon import responseJSON
import hashlib

def getDataUser(v_user):
  '''query SELECT data user berdasarkan nik '''
  customQuery = QueryStringDb("POSTGRES")
  v_query = '''SELECT USER_KTA, USER_NAMA, USER_ROLE, USER_PIN
        FROM DVD_STORE_USER
        WHERE USER_KTA = %s ''' 
  v_kondisi = (v_user,)
  v_hasil = customQuery.select(v_query, v_kondisi)
  print(v_hasil)
  return v_hasil

# def getDataUserWithPIN(v_user, v_pin):
#   '''query SELECT data user berdasarkan nik '''
#   customQuery = QueryStringDb("POSTGRES")
#   v_query = '''SELECT USER_KTA, USER_NAMA, USER_ROLE, USER_PIN
#         FROM DVD_STORE_USER
#         WHERE USER_KTA = %s AND USER_PIN = %s ''' 
#   v_kondisi = (v_user, v_pin, )
#   v_hasil = customQuery.select(v_query, v_kondisi)
#   # print(v_hasil)
#   return v_hasil

# def getDataUser(v_user):
#   '''query SELECT data user berdasarkan nik '''
#   customQuery = QueryStringDb("POSTGRES")
#   v_query = '''SELECT nik, kd_branch, kd_jabatan, act
#         FROM mrat_nik_giliran_app
#         WHERE nik = %s ''' 
#   v_kondisi = (v_user,)
#   v_hasil = customQuery.select(v_query, v_kondisi)
#   # print(v_hasil)
#   return v_hasil

def getLastID():
  customQuery = QueryStringDb("POSTGRES")
  try:
    select = '''
          SELECT LPAD(CAST(count(1)+1 AS varchar), 5, '0') AS NO_ID FROM DVD_STORE_TEST;
          '''
    v_hasil = customQuery.selectTanpaParam(select)
    return v_hasil
  except Exception as e:
    return responseJSON(400, 'F', str(e), [])

def upload_film(no_id_film, judul_film, category, rating, kualitas, descp, stock, user_buat, tgl_buat): 
  customQuery = QueryStringDb("POSTGRES")
  # print(customQuery)
  v_query = '''INSERT INTO DVD_STORE_TEST
          (DTL_ID_DVD, DTL_JUDUL_FILM, DTL_CATEGORY, DTL_RATING, DTL_KUALITAS, DTL_DESCP, DTL_STOCK, DTL_USER_BUAT, DTL_TGL_BUAT, DTL_STATUS_AKTIF )
          VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, 'T');
        '''
  v_kondisi = (no_id_film, judul_film, category, rating, kualitas, descp, stock, user_buat, tgl_buat, )
  print(v_kondisi)
  v_hasil = customQuery.execute(v_query, v_kondisi)
  return v_hasil

def getLastID_user():
  customQuery = QueryStringDb("POSTGRES")
  try:
    select = '''
          SELECT LPAD(CAST(count(1)+1 AS varchar), 5, '0') AS NO_ID FROM DVD_STORE_USER;
          '''
    v_hasil = customQuery.selectTanpaParam(select)
    return v_hasil
  except Exception as e:
    return responseJSON(400, 'F', str(e), [])

def getLastID_sewa():
  customQuery = QueryStringDb("POSTGRES")
  try:
    select = '''
          SELECT LPAD(CAST(count(1)+1 AS varchar), 5, '0') AS NO_ID FROM DVD_STORE_SEWA;
          '''
    v_hasil = customQuery.selectTanpaParam(select)
    return v_hasil
  except Exception as e:
    return responseJSON(400, 'F', str(e), [])

def proses_simpan_User(kta, nama, pin, tgl_buat): 
  customQuery = QueryStringDb("POSTGRES")
  # print(customQuery)
  v_query = '''INSERT INTO DVD_STORE_USER
          (USER_KTA, USER_NAMA, USER_PIN, USER_TGL_BUAT, USER_ROLE, USER_AKTIF )
          VALUES(%s, %s, %s, %s, 'CUS', 'T' );
        '''
  v_kondisi = (kta, nama, pin, tgl_buat, )
  print(v_kondisi)
  v_hasil = customQuery.execute(v_query, v_kondisi)
  return v_hasil

def getDataListFilm():
  customQuery = QueryStringDb("POSTGRES")
  try:
    vDataListFilm = '''
          SELECT DTL_ID_DVD, DTL_JUDUL_FILM, DTL_CATEGORY, DTL_RATING, DTL_KUALITAS, DTL_DESCP, DTL_STOCK, DTL_USER_BUAT, DTL_TGL_BUAT, DTL_STATUS_AKTIF
            FROM DVD_STORE_TEST order by DTL_TGL_BUAT
          '''
    v_hasil = customQuery.selectTanpaParam(vDataListFilm)
    return v_hasil
  except Exception as e:
    return responseJSON(400, 'F', str(e), [])
    # WHERE DTL_STATUS_AKTIF != 'F'

def getDataListFilmWithKondisi():
  customQuery = QueryStringDb("POSTGRES")
  try:
    vDataListFilm = '''
          SELECT DTL_ID_DVD, DTL_JUDUL_FILM, DTL_CATEGORY, DTL_RATING, DTL_KUALITAS, DTL_DESCP, DTL_STOCK, DTL_USER_BUAT, DTL_TGL_BUAT, DTL_STATUS_AKTIF
            FROM DVD_STORE_TEST WHERE DTL_STATUS_AKTIF != 'F' AND DTL_STOCK != '0' order by DTL_TGL_BUAT
          '''
    v_hasil = customQuery.selectTanpaParam(vDataListFilm)
    return v_hasil
  except Exception as e: 
    return responseJSON(400, 'F', str(e), [])
    

def getDetailFilm(no_id_film):
  customQuery = QueryStringDb("POSTGRES")
  try:
    vDetail = '''
          SELECT DTL_ID_DVD, DTL_JUDUL_FILM, DTL_CATEGORY, DTL_RATING, DTL_KUALITAS, DTL_DESCP, DTL_STOCK, DTL_STATUS_AKTIF
            FROM DVD_STORE_TEST
          where DTL_ID_DVD = %(vno_id_film)s
          '''
    v_kondisi = {"vno_id_film":no_id_film.upper()}
    v_hasil = customQuery.select(vDetail, v_kondisi)
    return v_hasil
  except Exception as e:
    return responseJSON(400, 'F', str(e), [])

def proses_hapus_film(user_hapus, tgl_update, no_id_film ):
  customQuery = QueryStringDb("POSTGRES")
  try:
    vQueryDelete = '''UPDATE DVD_STORE_TEST
          SET DTL_STATUS_AKTIF = 'F', DTL_USER_UPDATE = %s, DTL_TGL_UPDATE = %s
          WHERE DTL_ID_DVD = %s '''
    vKondisi = (user_hapus, tgl_update, no_id_film,)
    vHasilDelete = customQuery.execute(vQueryDelete, vKondisi)
    return vHasilDelete
  except Exception as e:
    return responseJSON(400, 'F', str(e), [])

def proses_update_film(judul_film, category, descp, rating, kualitas, stock, status, user_update, tgl_update, no_id_film):
  customQuery = QueryStringDb("POSTGRES")
  try:
    vQuery = '''UPDATE DVD_STORE_TEST
          SET DTL_JUDUL_FILM = %s, DTL_CATEGORY = %s, DTL_DESCP = %s, DTL_RATING = %s, DTL_KUALITAS =%s, DTL_STOCK = %s, 
          DTL_STATUS_AKTIF = %s, DTL_USER_UPDATE = %s, DTL_TGL_UPDATE = %s
          WHERE DTL_ID_DVD = %s '''
    vKondisi = (judul_film, category, descp, rating, kualitas, stock, status, user_update, tgl_update, no_id_film,)
    vHasilDelete = customQuery.execute(vQuery, vKondisi)
    return vHasilDelete
  except Exception as e:
    return responseJSON(400, 'F', str(e), [])

def sewa_film(no_id_sewa, no_id_film, user_sewa, tgl_buat, nama_file):
  customQuery = QueryStringDb("POSTGRES")
  # print(customQuery)
  v_query = '''INSERT INTO DVD_STORE_SEWA
          (SEWA_ID, SEWA_ID_DVD, SEWA_ID_USER, SEWA_TGL_BUAT, SEWA_FILE, SEWA_STATUS )
          VALUES(%s, %s, %s, %s, %s, 'F' );
        '''
  v_kondisi = (no_id_sewa, no_id_film, user_sewa, tgl_buat, nama_file, )
  print(v_kondisi)
  v_hasil = customQuery.execute(v_query, v_kondisi)
  return v_hasil

def getStock(no_id_film):
  customQuery = QueryStringDb("POSTGRES")
  try:
    vQuery = '''SELECT DTL_STOCK FROM DVD_STORE_TEST
          WHERE DTL_ID_DVD = %s '''
    vKondisi = (no_id_film,)
    v_hasil = customQuery.select(vQuery, vKondisi)
    return v_hasil
  except Exception as e:
    return responseJSON(400, 'F', str(e), [])

def update_stock(kurang_stock, no_id_film):
  customQuery = QueryStringDb("POSTGRES")
  try:
    vQuery = '''UPDATE DVD_STORE_TEST
          SET DTL_STOCK = %s
          WHERE DTL_ID_DVD = %s '''
    vKondisi = (kurang_stock, no_id_film,)
    vHasilDelete = customQuery.execute(vQuery, vKondisi)
    return vHasilDelete
  except Exception as e:
    return responseJSON(400, 'F', str(e), [])

def getDataListSewa():
  customQuery = QueryStringDb("POSTGRES")
  try:
    vDataListSewa = '''
          SELECT DTL_ID_DVD, DTL_JUDUL_FILM, DTL_CATEGORY, DTL_RATING, DTL_KUALITAS, DTL_DESCP, DTL_STOCK, DTL_USER_BUAT, DTL_TGL_BUAT, DTL_STATUS_AKTIF, 
          SEWA_ID, SEWA_ID_DVD, SEWA_ID_USER, SEWA_TGL_BUAT, SEWA_FILE, SEWA_STATUS 
          FROM DVD_STORE_SEWA JOIN DVD_STORE_TEST ON DTL_ID_DVD = SEWA_ID_DVD order by SEWA_TGL_BUAT
          '''
    v_hasil = customQuery.selectTanpaParam(vDataListSewa)
    return v_hasil
  except Exception as e:
    return responseJSON(400, 'F', str(e), [])

def getDetailSewa(no_id_sewa):
  customQuery = QueryStringDb("POSTGRES")
  try:
    vDetail = '''
          SELECT DTL_ID_DVD, DTL_JUDUL_FILM, DTL_CATEGORY, DTL_RATING, DTL_KUALITAS, DTL_DESCP, DTL_STOCK, DTL_USER_BUAT, DTL_TGL_BUAT, DTL_STATUS_AKTIF, 
          SEWA_ID, SEWA_ID_DVD, SEWA_ID_USER, SEWA_TGL_BUAT, SEWA_FILE, SEWA_STATUS, SEWA_TGL_UPDATE
          FROM DVD_STORE_SEWA JOIN DVD_STORE_TEST ON DTL_ID_DVD = SEWA_ID_DVD
          where SEWA_ID = %(vno_id_sewa)s
          '''
    v_kondisi = {"vno_id_sewa":no_id_sewa.upper()}
    v_hasil = customQuery.select(vDetail, v_kondisi)
    return v_hasil
  except Exception as e:
    return responseJSON(400, 'F', str(e), [])

def update_detail_pengajuan(id_app, tgl_app, no_id_sewa):
  customQuery = QueryStringDb("POSTGRES")
  try:
    vQuery = '''UPDATE DVD_STORE_SEWA
          SET SEWA_STATUS = 'DELIV', SEWA_ID_UPDATE = %s , SEWA_TGL_UPDATE = %s
          WHERE SEWA_ID = %s '''
    vKondisi = (id_app, tgl_app, no_id_sewa, )
    vHasilDelete = customQuery.execute(vQuery, vKondisi)
    return vHasilDelete
  except Exception as e:
    return responseJSON(400, 'F', str(e), [])


def update_detail_pengajuan_tolak(id_app, tgl_app, no_id_sewa):
  customQuery = QueryStringDb("POSTGRES")
  try:
    vQuery = '''UPDATE DVD_STORE_SEWA
          SET SEWA_STATUS = 'REJECT', SEWA_ID_UPDATE = %s , SEWA_TGL_UPDATE = %s
          WHERE SEWA_ID = %s '''
    vKondisi = (id_app, tgl_app, no_id_sewa, )
    vHasilDelete = customQuery.execute(vQuery, vKondisi)
    return vHasilDelete
  except Exception as e:
    return responseJSON(400, 'F', str(e), [])

    

def getDataListSewaCUS(id_user):
  customQuery = QueryStringDb("POSTGRES")
  try:
    vQuery = '''
          SELECT DTL_ID_DVD, DTL_JUDUL_FILM, DTL_CATEGORY, DTL_RATING, DTL_KUALITAS, DTL_DESCP, DTL_STOCK, DTL_USER_BUAT, DTL_TGL_BUAT, DTL_STATUS_AKTIF, 
          SEWA_ID, SEWA_ID_DVD, SEWA_ID_USER, SEWA_TGL_BUAT, SEWA_FILE, SEWA_STATUS 
          FROM DVD_STORE_SEWA JOIN DVD_STORE_TEST ON DTL_ID_DVD = SEWA_ID_DVD where SEWA_ID_USER = %s order by SEWA_TGL_BUAT
          '''
    vKondisi = (id_user,)
    v_hasil = customQuery.select(vQuery, vKondisi)
    return v_hasil
  except Exception as e:
    return responseJSON(400, 'F', str(e), [])

def update_detail_pengembalian(id_app, tgl_app, no_id_sewa):
  customQuery = QueryStringDb("POSTGRES")
  try:
    vQuery = '''UPDATE DVD_STORE_SEWA
          SET SEWA_STATUS = 'DONE', SEWA_ID_UPDATE = %s , SEWA_TGL_UPDATE = %s
          WHERE SEWA_ID = %s '''
    vKondisi = (id_app, tgl_app, no_id_sewa, )
    vHasilDelete = customQuery.execute(vQuery, vKondisi)
    return vHasilDelete
  except Exception as e:
    return responseJSON(400, 'F', str(e), [])

def getLastID_history():
  customQuery = QueryStringDb("POSTGRES")
  try:
    select = '''
          SELECT LPAD(CAST(count(1)+1 AS varchar), 5, '0') AS NO_ID FROM DVD_HISTORY_SEWA;
          '''
    v_hasil = customQuery.selectTanpaParam(select)
    return v_hasil
  except Exception as e:
    return responseJSON(400, 'F', str(e), [])

def insert_history(no_id_history, no_id_film, id_app, feedback, rating, tgl_buat, no_id_sewa):
  customQuery = QueryStringDb("POSTGRES")
  # print(customQuery)
  v_query = '''INSERT INTO DVD_HISTORY_SEWA
          (HISTORY_ID, HISTORY_ID_DVD, HISTORY_ID_USER, HISTORY_FEEDBACK, HISTORY_RATING, HISTORY_TGL_BUAT, HISTORY_ID_SEWA, HISTORY_STATUS )
          VALUES(%s, %s, %s, %s, %s, %s, %s, 'DONE' );
        '''
  v_kondisi = (no_id_history, no_id_film, id_app, feedback, rating, tgl_buat, no_id_sewa, )
  print(v_kondisi)
  v_hasil = customQuery.execute(v_query, v_kondisi)
  return v_hasil

