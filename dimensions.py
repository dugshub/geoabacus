from app import app, db
from app.models import DimensionTags, Dimension, dimensions_schema, dimension_schema, dimension_tags_schema, \
    metrics_schema
from flask import abort
import lkml
import looker_models as lm


def read_all():
    with app.app_context():
        dim_tags = db.session.query(DimensionTags).all()
        return dimension_tags_schema.dump(dim_tags)


def create(dimension):
    dimensions = [dimension.name for dimension in db.session.query(Dimension).all()]
    name = dimension.get("name")
    type = dimension.get("type")

    if name and name not in dimensions:
        dim = Dimension(
            name=name,
            type=type
        )
        with app.app_context():
            db.session.add(dim)
            db.session.commit()
        return dimension_schema.dump(dim)

    else:
        abort(406, "Dimension already exists")


def generate_lookml(fields):
    metrics = fields.get('metrics')
    dimensions = fields.get('dimensions')

    with app.app_context(), db.session.no_autoflush:
        metrics = metrics_schema.load(metrics)
        dimensions = dimensions_schema.load(dimensions)

    tablename = "rental_performance"
    schema = "dbt_looker"
    sql_trigger_value = "SELECT FLOOR(((TIMESTAMP_DIFF(CURRENT_TIMESTAMP(),'1970-01-01 00:00:00',SECOND)) - 60*60*10)/(60*60*24))"
    derived_table = {}
    derived_table['sql'] = f"select * from {schema}.{tablename}"
    derived_table['sql_trigger_value'] = sql_trigger_value
    derived_table = {"derived_table": derived_table}

    view = {"name": tablename}

    view.update(derived_table)
    #view.update({"measures": [lm.to_looker(metric) for metric in metrics]})
    view.update({"dimensions": [lm.to_looker(dimension) for dimension in dimensions]})

    view = {"view": view}
    print(view)
    print(type(view))
    lookml = lkml.dump(view)
    #
    with open('explore.lkml', 'w') as f:
        for line in lookml:
            f.write(f"{line}")

    return lookml

