from app.models import DimensionTags, Dimension
from app import app, db
import pandas as pd
import numpy as np
from sqlalchemy import select, and_, or_

tags = pd.read_csv('tags.csv')
tags = tags.replace({np.nan: None})

with app.app_context():
    stmt = select(DimensionTags)
    existing_names = db.session.execute(stmt).scalars().all()
    existing_names = [dimensionTag.name for dimensionTag in existing_names]

    for tag in tags.itertuples():
        print (tag.name)

        if tag.name in existing_names:
            print('exists, updating current record.')
            existing = db.session.get(Dimension,tag.name)
            existing = DimensionTags(
                name=tag.name,
                primary_tag=tag.primary_tag,
                secondary_tag=tag.secondary_tag,
                data_group=tag.data_group,
            )
        else:
            db.session.add(
                DimensionTags(
                    name=tag.name,
                    primary_tag=tag.primary_tag,
                    secondary_tag=tag.secondary_tag,
                    data_group=tag.data_group,
                )
            )

    db.session.commit()