import os

import geojson
import sqlalchemy as sa
from sqlalchemy import text

wofdb = os.environ.get("WOF_SQLITE_PATH")
engine = sa.create_engine(f'sqlite:///{wofdb}')


def get_by_placetype(placetype_filter=('country','region','county')):
    """
    Returns a list of sqlalchemy.engine.row.RowMapping items of WhosOnFirst geojson blobs using placetype as a filter.
    Only pulls locations marked as 'is_current'

    Args:
        None - tbd

    Returns:
        list: Objects of WhosOnFirst data. Can be indexed as a dictionary or through attribute notation.
    """
    with engine.connect() as connection:
        query = text(
            f"""
            with
            dims as (
                select id from spr
                         where placetype in {placetype_filter} and
                               is_current
            ),
        
            shapes as (
                select
                    geojson.body as geojson_data
                from geojson
                where id in (select * from dims) and
                      not is_alt
            )

            select distinct * from shapes
         """
        )
        result = connection.scalars(query).all()
        row = [geojson.loads(row) for row in result]
        return row


def from_ids(wof_ids=[None]):
    """
    Returns a list of sqlalchemy.engine.row.RowMapping items of WhosOnFirst geojson blobs from a list of
    WhosOnFirst ids.

    Args:
        List of WhosOnFirst ids.

    Returns:
        list: Objects of WhosOnFirst data. Can be indexed as a dictionary or through attribute notation.
    """

    wof_ids = wof_ids or []
    with engine.connect() as connection:
        query = text(
            f"""
                with wof_ids as (
                    select id from spr
                        where
                            is_current = 1 and 
                            id in {wof_ids}
                ),
                shapes as (
                    select * from geojson
                )
                select  
                    body as geojson_data
                from shapes
                where not shapes.is_alt and
                shapes.id in (select * from wof_ids)
             """
        )
        result = connection.scalars(query).all()
        return [geojson.loads(row) for row in result]

def get_related_placetypes(wof_ids=(101735835, ''), placetypes=('neighbourhood', '')):
    """
    Returns a list of WhosOnFirst geojson objects.

    Args:
        List of WhosOnFirst ids.

    Returns:
        list: Objects of WhosOnFirst data. Can be indexed as a dictionary or through attribute notation.
    """

    with engine.connect() as connection:
        query = text(
            f"""
                with
                    dims as (
                        select * from spr
                    ),
                
                    parents as (
                    select *
                    from ancestors
                    where id in {wof_ids} and
                          ancestor_placetype in {placetypes} and
                          ancestor_id != id
                    ),
                
                    children as (
                    select ancestors.id as child_id,
                           dims.placetype as child_placetype,
                           ancestors.ancestor_id,
                           ancestors.ancestor_placetype
                    from ancestors
                        left join dims on dims.id = ancestors.id
                    where ancestor_id in {wof_ids} and
                          is_current and
                          placetype in {placetypes} and
                          child_id != ancestors.ancestor_id
                    ),
           
                    parents_and_children as (
                        select ancestor_id as wof_id
                        from parents
                
                        union all
                
                        select child_id as wof_id
                        from
                            children
                    ),
                
                    shapes as (
                        select
                            geojson.body as geojson_data
                        from geojson
                        where id in (select * from parents_and_children) and
                              not is_alt
                    )
                    
                    select distinct * from shapes

             """
        )
        result = connection.execute(query)
        connection.close()
        row = [geojson.loads(row._mapping.geojson_data) for row in result.fetchall()]
        return row
