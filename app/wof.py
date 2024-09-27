import os

import geojson
import sqlalchemy as sa
from sqlalchemy import text

wofdb = os.environ.get("WOF_SQLITE_PATH")

def get_placetypes(placetype_filter=None, name_filter=None, country_filter=None, region_filter=None):
    """
        Returns a list of sqlalchemy.engine.row.RowMapping items of WhosOnFirst geojson blobs using placetype as a filter.
        Only pulls locations marked as 'is_current'

        Args:
            None - tbd

        Returns:
            list: Objects of WhosOnFirst data. Can be indexed as a dictionary or through attribute notation.
        """

    engine = sa.create_engine(f'sqlite:///{wofdb}')
    with engine.connect() as connection:
        query = text(
                f"""
                    with 
                        dims as (
                            select *
                            from spr
                            where placetype in ('{placetype_filter.lower()}') and
                            lower(name) in ('{name_filter.lower()}') and
                            lower(country) in ('{country_filter.lower()}') and
                            is_current != 0 ),
                    
                             shapes as (select id,
                       geojson.body as geojson_data
                    from geojson
                    where id in (select id from dims)
                      and not is_alt),

                final as (select distinct shapes.id,
                               dims.name,
                               dims.placetype,
                               region_spr.name as region,
                               locality_spr.name as locality,
                               dims.country,
                               local_hierarchy.ancestor_id  as locality_id,
                               region_hierarchy.ancestor_id as region_id,
                               shapes.geojson_data
               from shapes
                        left join dims on shapes.id = dims.id
                        left join ancestors local_hierarchy on local_hierarchy.id = shapes.id
                            and local_hierarchy.ancestor_placetype = 'locality'
                        left join ancestors region_hierarchy on region_hierarchy.id = shapes.id
                            and region_hierarchy.ancestor_placetype = 'region'
                        left join spr region_spr on region_hierarchy.ancestor_id = region_spr.id
                        left join spr locality_spr on local_hierarchy.ancestor_id = locality_spr.id
                )   
                select *
                from final;
                    """
                )
        results = connection.execute(query).all()
        rows = [geojson.loads(row.geojson_data) for row in results]
        return rows, results


def get_by_placetype(placetype_filter=('country','region','county')):

    """
    Returns a list of sqlalchemy.engine.row.RowMapping items of WhosOnFirst geojson blobs using placetype as a filter.
    Only pulls locations marked as 'is_current'

    Args:
        None - tbd

    Returns:
        list: Objects of WhosOnFirst data. Can be indexed as a dictionary or through attribute notation.
    """

    engine = sa.create_engine(f'sqlite:///{wofdb}')
    with engine.connect() as connection:
        query = text(
            f"""
            with
            dims as (
                select id from spr
                         where placetype in {placetype_filter} and
                               is_current != 0 
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


def from_ids(wof_ids, include_alt_geom=False):
    alt_geom = ''
    if not include_alt_geom:
        alt_geom = 'and not shapes.is_alt'

    if not isinstance(wof_ids, list):
        if isinstance(wof_ids, int):
            wof_ids = [wof_ids,'']

    if len(wof_ids) == 1:
        wof_ids.append('')
    wof_ids = tuple(wof_ids)

    """
    Returns a list of sqlalchemy.engine.row.RowMapping items of WhosOnFirst geojson blobs from a list of
    WhosOnFirst ids.

    Args:
        List of WhosOnFirst ids.

    Returns:
        list: Objects of WhosOnFirst data. Can be indexed as a dictionary or through attribute notation.
    """

    engine = sa.create_engine(f'sqlite:///{wofdb}')
    wof_ids = wof_ids or []
    with engine.connect() as connection:
        query = text(
            f"""
                with wof_ids as (
                    select id from spr
                        where
                            is_current != 0  and 
                            id in {wof_ids}
                ),
                shapes as (
                    select * from geojson
                )
                select  
                    body as geojson_data
                from shapes
                where shapes.id in (select * from wof_ids)  
                {alt_geom}
             """
        )
        results = connection.scalars(query).all()
        if include_alt_geom:
            return [geojson.loads(result) for result in results if geojson.loads(result).geometry.type not in ['Point']]
        #return [geojson.loads(row) for row in results if geojson.loads(row).geometry.type not in ['Point']]
        #return _extract_correct_geojson(results)
        return [geojson.loads(row) for row in results]

def from_id(wof_id):
    if not isinstance(wof_id, str):
        wof_id = int(wof_id)

    return from_ids(wof_id)[0]

def _extract_correct_geojson(rows):
    pass

def get_related_placetypes(wof_ids=(101735835, ''), placetypes=('neighbourhood', '')):
    """
    Returns a list of WhosOnFirst geojson objects.

    Args:
        List of WhosOnFirst ids.

    Returns:
        list: Objects of WhosOnFirst data. Can be indexed as a dictionary or through attribute notation.
    """
    engine = sa.create_engine(f'sqlite:///{wofdb}')
    with engine.connect() as connection:
        query = text(
            f"""
                with
                    dims as (
                        select * from spr
                        where is_current != 0 
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
                          is_current != 0  and
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
