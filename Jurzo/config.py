class Config:
    SECRET_KEY = 'fd1690f36c025ca204c6fececc84db4d'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'a.aadharsh2002@gmail.com'
    MAIL_PASSWORD = 'workhardstayhumblespreadlove'

    def __init__(self):
        if os.environ.get('DATABASE_URL') is None:
            SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
                os.path.join(basedir, 'app.db')
        else:
            SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
