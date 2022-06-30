from os import environ
import os


class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    SECRET_KEY = "48fc01ae9e3a6d0df92d4fe42eaa2b1d"
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('env')

    
    folderUpload = 'files'
    ALLOWED_EXTENSIONS = set(['pdf','zip','rar','7Z','7z'])
    
    # Database
    SQLALCHEMY_DATABASE_URI=''
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    
