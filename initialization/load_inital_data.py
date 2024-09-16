from app import app,db,ma
from os import listdir
from os.path import isfile, join

wof_databases = [f for f in listdir(mypath) if isfile(join(mypath, f))]