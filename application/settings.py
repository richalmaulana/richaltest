import os

#konfigurasi aplikasi
SECRET_KEY="richal12345" # secret key aplikasi
PASSWORD_ROOT = '12345' # password sakti aplikasi buat by pass login

#jika menggunakan SQL ALCHEMY(ORM)
SQLALCHEMY_TRACK_MODIFICATIONS=False
# SQLALCHEMY_DATABASE_URI="postgresql://<user>:<password>@<host>:<port>/<sid>"

USER_POSTGRES_DB = "postgres"
PASSWORD_POSTGRES_DB = "rchlmln"
HOST_POSTGRES_DB = "localhost"
PORT_POSTGRES_DB = "5432"
DATABASE_POSTGRES_DB = "postgres"

FILE_UPLOADS = "D:/work python/richal_test/file"
FILE_BUKTI_SEWA = "D:/work python/richal_test/file_bukti_sewa"
