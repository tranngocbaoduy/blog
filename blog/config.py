import os

class Config:   
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGODB_USERNAME = str(os.environ.get('MONGODB_USERNAME'))
    MONGODB_PASSWORD = str(os.environ.get('MONGODB_PASSWORD'))

    MONGODB_DB = 'db-ai-search'
  
    MONGODB_HOST = 'mongodb+srv://'+ MONGODB_USERNAME +':'+ MONGODB_PASSWORD +'@cluster0-qz9ip.mongodb.net/db-ai-search?retryWrites=true'
  
    # mail server
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD =  os.environ.get('MAIL_PASSWORD')
