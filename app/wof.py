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
                    select * from spr
                        where
                            is_current = 1 and 
                            id in {wof_ids}
                ),
                
                hierarchy as (
                    select * from ancestors
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
        connection.close()
        return [row._mapping for row in result.fetchall()]


def get_related_placetypes(wof_ids=(101735835, ''), placetypes=('neighbourhood', '')):
    """
    Returns a list of sqlalchemy.engine.row.RowMapping items of WhosOnFirst geojson blobs from a list of
    WhosOnFirst ids. This function will pull all associated placetypes (

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
        return [row._mapping for row in result.fetchall()]
