from app import app, db
from app.models import DimensionTags, Dimension, dimensions_schema, dimension_schema, dimension_tags_schema, \
    metrics_schema
from flask import abort


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

    with db.session.no_autoflush:
        dims = dimensions_schema.load(dimensions)
        metriz = metrics_schema.load(metrics)

    return metrics_schema.dump(metriz)
