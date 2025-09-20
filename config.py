import os

class Config:
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345678@localhost:5432/student_reg'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret'