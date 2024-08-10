import numpy as np
import pandas as pd
import lkml

from app import app, db, ma
from app.models import Dimension, dimension_schema

dimensions = pd.read_csv('tags.csv')
dimensions = dimensions.replace({np.nan: None})

print(dimensions.head())

# with app.app_context():
#     for id, dimensions in dimensions.iterrows():
#         db.session.add(Dimension(
#             name=dimensions['name'],
#             primary_tag=dimensions['primary_tag'],
#             secondary_tag=dimensions['secondary_tag'],
#             type=dimensions['type'],
#             data_group='core'
#         ))
#     db.session.commit()

with app.app_context():
    dimension = db.session.query(Dimension).first()
#
dim = dimension_schema.dump(dimension)

print(dim)
# with open('explore.lkml', 'r') as file:
#    result = lkml.load(file)
#
# dim = {"dimension": dim}
dimenz = {
    "dimension": {
        "type": "number",
        "label": "Unit Price",
        "sql": "${TABLE}.price",
        "name": "price"
    }
}
print(dimension)
print(lkml.dump(dimenz))
#FIGURE OUT WHY THE BELOW FAILS

print(dimension.to_lkml())
