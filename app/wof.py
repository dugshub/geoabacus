import os

import sqlalchemy as sa
from sqlalchemy import text

wofdb = os.environ.get("WOF_SQLITE_PATH")
engine = sa.create_engine(f'sqlite:///{wofdb}')
def get_geojson(query=None):
    """
    Returns a list of sqlalchemy.engine.row.RowMapping items of WhosOnFirst geojson blobs.

    Args:
        None - tbd

    Returns:
        list: Objects of WhosOnFirst data. Can be indexed as a dictionary or through attribute notation.
    """
    with engine.connect() as connection:
        query = query or text(
            """
            with wof_ids as (
                select * from spr
                    where
                        placetype = "locality" and
                        name = "Toronto" and
                        country = "CA" and
                        is_current = 1
            ),

                shapes as (
                    select * from geojson
                )

            select  
                wof_ids.id,
                parent_id as parent,
                name,
                placetype,
                country,
                body as geojson,
                is_current,
                is_alt
            from wof_ids
            left join shapes on wof_ids.id = shapes.id
            where not shapes.is_alt 
         """
        )
        result = connection.execute(query)
        return [row._mapping for row in result.fetchall()]
