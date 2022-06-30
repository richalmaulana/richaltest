import psycopg2
# import cx_Oracle
from application import app

def responseJSON(status_code, flag, message , result):
	resp = {}
	resp['status_code'] = status_code
	resp['status'] = flag
	resp['message'] = message
	resp['result'] = result
	return resp

def rows_to_dict_list(cursor):
	''' Function return list of dictionary  '''
	columns = [i[0].lower() for i in cursor.description]
	return [dict(zip(columns, row)) for row in cursor]

class QueryStringDb(object):
	def __init__(self, jenis_db):
		if (jenis_db == "POSTGRES"):
			self._db_connection = psycopg2.connect(user=app.config["USER_POSTGRES_DB"],password=app.config["PASSWORD_POSTGRES_DB"],
										host=app.config["HOST_POSTGRES_DB"],port=app.config["PORT_POSTGRES_DB"],
										database=app.config["DATABASE_POSTGRES_DB"])
			self._db_cursor = self._db_connection.cursor()
		else:
			self._dsn_tns = None
			self._db_connection = None
			self._db_cursor = None
		
	def __del__(self):
		self._db_cursor.close()
		self._db_connection.close()

	def select(self, p_query, p_param):
		try:
			self._sqlQuery = p_query
			self._v_kondisi = p_param 
			self._db_cursor.execute(self._sqlQuery, self._v_kondisi)
			self._result = rows_to_dict_list(self._db_cursor) 
			return responseJSON(200,"T","Sukses",self._result)
		except Exception as error:
			return responseJSON(200,"F",str(error),[])

	def selectTanpaParam(self, p_query):
		try:
			self._sqlQuery = p_query
			self._db_cursor.execute(self._sqlQuery)
			self._result = rows_to_dict_list(self._db_cursor) 
			return responseJSON(200,"T","Sukses",self._result)
		except Exception as error:
			return responseJSON(200,"F",str(error),[])

	def execute(self, p_query, p_param, p_pesan="Proses Berhasil"):
		try:
			self._sqlQuery = p_query
			self._v_kondisi = p_param 
			self._db_cursor.execute(self._sqlQuery, self._v_kondisi)
			self._db_connection.commit()
			return responseJSON(200,"T",p_pesan,None)
		except Exception as error:
			self._db_connection.rollback()
			return responseJSON(200,"F",str(error),None)
