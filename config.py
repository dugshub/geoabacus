import os
from pathlib import Path
from dotenv import load_dotenv

######
basedir = Path(__file__).parent.absolute()
load_dotenv(dotenv_path=".env_dev")
placetype_hierarchy = ('country','region','locality','neighbourhood')
######

class Config:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{basedir}/databases/{os.environ.get('SQLITE_DATABASE_NAME')}' or \
                              'sqlite:///' + os.path.join(basedir, '/databases/app.db')

