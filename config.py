import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))
print(f'sqlite:///{basedir}' + f"{os.environ.get('SQLITE_DATABASE_PATH')}")

class Config:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{basedir}' + f"{os.environ.get('SQLITE_DATABASE_PATH')}" or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')

    #WOF_DATABASE_URI = f'sqlite:///{basedir}' + f"{os.environ.get('WOF_DATABASE_PATH')}"
