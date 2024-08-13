from string import capwords
from typing import Optional

from marshmallow import fields, pre_load
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped

from app import db, ma


class DimensionTags(db.Model):
    id: Mapped[int] = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name: Mapped[str] = db.Column(db.String, db.ForeignKey('dimension.name'), nullable=False, unique=True)
    primary_tag: Mapped[Optional[str]] = db.Column(db.String, nullable=True)
    secondary_tag: Mapped[Optional[str]] = db.Column(db.String, nullable=True)
    data_group: Mapped[[Optional[str]]] = db.Column(db.String, nullable=True)

    __table_args__ = (UniqueConstraint("name", name="fk_unique_constraint"),)

    def __init__(self, name: str, primary_tag: Optional[str], secondary_tag: Optional[str], data_group: Optional[str]):
        self.name = name
        self.primary_tag = primary_tag
        self.secondary_tag = secondary_tag
        self.data_group = data_group

    def __repr__(self):
        return '<DimensionTag{}>'.format(self.name, self.primary_tag, self.secondary_tag, self.data_group)


class DimensionTagsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DimensionTags
        load_instance = True
        sqla_session = db.session
        include_fk = True


class Dimension(db.Model):
    name: Mapped[str] = db.Column(db.String, nullable=False, primary_key=True)
    type: Mapped[str] = db.Column(db.String, nullable=False)
    label: Mapped[Optional[str]] = None
    description: Mapped[Optional[str]] = None
    qualifiedName: Mapped[Optional[str]] = db.Column(db.String, nullable=True)

    dimensionTags = db.relationship('DimensionTags', back_populates='dimension', cascade="all, delete-orphan",
                                    uselist=False)

    def __init__(self, name: str, type: str, label: Optional[str] = None, description: Optional[str] = None
                 , qualifiedName: Optional[str] = None, dimensionTags: DimensionTags = None):
        self.name = name
        self.type = type
        self.label = label or capwords(self.name.split('__')[-1].replace('_', ' '))
        self.description = description
        self.qualifiedName = qualifiedName
        self.dimensionTags = dimensionTags

    def __repr__(self):
        return '<Dimension {}>'.format(self.name)


DimensionTags.dimension = db.relationship('Dimension', back_populates='dimensionTags', single_parent='True')


class DimensionSchema(ma.SQLAlchemyAutoSchema):
    # queryableGranularities = fields.List(fields.Str() or None)
    class Meta:
        model = Dimension
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    dimensionTags = fields.Nested("DimensionTagsSchema", many=False, allow_none=True)


##### METRICS ######

class MetricTags(db.Model):
    id: Mapped[int] = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name: Mapped[str] = db.Column(db.String, db.ForeignKey('metric.name'), nullable=False, unique=True)
    metric_type: Mapped[Optional[str]] = db.Column(db.String, nullable=True)
    metric_category: Mapped[Optional[str]] = db.Column(db.String, nullable=True)
    group: Mapped[Optional[str]] = db.Column(db.String, nullable=True)

    __table_args__ = (UniqueConstraint("name", name="fk_unique_constraint_metric"),)

    def __init__(self, name: str, metric_type: Optional[str], metric_category: Optional[str],group: Optional[str]):
        self.name = name
        self.metric_type = metric_type
        self.metric_category = metric_category
        self.group = group

    def __repr__(self):
        return '<DimensionTag{}>'.format(self.name)


class MetricTagsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MetricTags
        load_instance = True
        sqla_session = db.session
        include_fk = True


class Metric(db.Model):
    name: Mapped[str] = db.Column(db.String, nullable=False, primary_key=True)
    type: Mapped[str] = db.Column(db.String, nullable=False)
    label: Mapped[Optional[str]] = None
    description: Mapped[Optional[str]] = None

    metricTags = db.relationship('MetricTags', back_populates='metric', cascade="all, delete-orphan",
                                 uselist=False)

    def __init__(self, name: str, type: str, label: Optional[str] = None, description: Optional[str] = None
                 , metricTags: metricTags = None):
        self.name = name
        self.type = type
        self.label = label or capwords(self.name.split('__')[-1].replace('_', ' '))
        self.description = description
        self.metricTags = metricTags

    def __repr__(self):
        return '<Metric {}>'.format(self.name)


MetricTags.metric = db.relationship('Metric', back_populates='metricTags', single_parent='True')


class MetricSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Metric
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    @pre_load(pass_many=True)
    def prep_metrics(self, data, many, **kwargs):
        for idx, metric in enumerate(data):
            metric_tag = {'metricTags': metric['config']['meta']}
            metric_tag['metricTags']['name'] = metric['name']

            data[idx].pop('config')
            data[idx].update(metric_tag)

        return data


    metricTags = fields.Nested("MetricTagsSchema", many=False, allow_none=True)


dimension_schema = DimensionSchema()
dimensions_schema = DimensionSchema(many=True)
dimension_tag_schema = DimensionTagsSchema(exclude=("id",))
dimension_tags_schema = DimensionTagsSchema(many=True, exclude=("id",))

metric_schema = MetricSchema()
metrics_schema = MetricSchema(many=True)
metric_tag_schema = MetricTagsSchema(exclude=("id",))
metric_tags_schema = MetricTagsSchema(many=True, exclude=("id",))
