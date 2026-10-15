import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'chave-padrao-dev-insegura')
    
    # Suporte flexível para SQLite e PostgreSQL
    db_url = os.getenv('DATABASE_URL', 'sqlite:///emprestados.db')
    # Ajuste caso a URI use 'postgres://' (comum em provedores como Heroku/Render)
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
        
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Credenciais do Sentry
    SENTRY_DSN = os.getenv('SENTRY_DSN', '')
