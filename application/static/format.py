def rows_to_dict(cursor):
	columns = [i[0].lower() for i in cursor.description]
	for row in cursor:
		hasil = dict(zip(columns, row))
	return hasil

def rows_to_dict_list(cursor):
	columns = [i[0].lower() for i in cursor.description]
	return [dict(zip(columns, row)) for row in cursor]