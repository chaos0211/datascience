# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/dbname'
    SQLALCHEMY_TRACK_MODIFICATIONS = False