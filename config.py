import os
from pathlib import Path
from dotenv import load_dotenv

######
basedir = Path(__file__).parent.absolute()
load_dotenv(dotenv_path=".env_dev")
print(f'sqlite:///{basedir}/{os.environ.get('SQLITE_DATABASE_PATH')}')

######

class Config:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{basedir}/{os.environ.get('SQLITE_DATABASE_PATH')}' or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')

