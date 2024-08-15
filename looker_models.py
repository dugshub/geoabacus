import re

from app.models import Dimension, Metric


def to_looker(field):
    field_type = type(field)

    if field_type == Dimension:
        return to_looker_dimension(field)

    if field_type == Metric:
        return to_looker_measure(field)


def to_looker_dimension(dimension: Dimension):
    dim = {
        "type": convert_type(dimension),
        "label": dimension.label,
        "description": dimension.description or "",
        "sql": f"${{TABLE}}.{dimension.name}",
        "name": dimension.name

    }

    return dim


def convert_type(dimension):
    if dimension.type == 'CATEGORICAL':
        return 'string'

    else:
        return 'date'


def to_looker_measure(metric: Metric):
    lookml_metric = {
        "label": metric.label,
        "description": metric.description or "",
        "sql": f"${{TABLE}}.{metric.name}",
        "name": metric.name,
    }

    properties = convert_metric_type(metric)
    [lookml_metric.update(property) for property in properties]

    return lookml_metric


def convert_metric_type(metric):
    properties = []

    if metric.type == 'SIMPLE':
        if hasattr(metric, 'measures'):
            agg = metric.measures[0]['agg']
        if agg == "SUM" or agg == "COUNT":
            properties.append({"type": agg.lower()})


        elif agg == "COUNT_DISTINCT" or agg == "SUM_DISTINCT":
            properties.append({"type": "SUM_DISTINCT"})
            properties.append({"sql_distinct_key": f"${{{_get_distinct_identity(metric)}}}"})

        elif agg == "AVG":
            return "havent built this yet"

    elif metric.type == "DERIVED":
            expr = metric.typeParams['expr']
            # Regular expression to find word-like strings that are not inside ${}
            pattern = r'(\b\w+\b)(?![^${]*})'
            result = re.sub(pattern, r'${\1}', expr)
            properties.append({"sql": result})

    elif metric.type == "RATIO":
        pass

    return properties


def _get_distinct_identity(metric):
    sql_string = metric.measures[0]['expr']
    entities = metric.entities
    pattern = r'CASE\s+WHEN\s+\S+\s+THEN\s+(\S+)\s+ELSE\s+(\S+)\s+END'

    match = re.search(pattern, sql_string, re.IGNORECASE)

    if match:
        then_value = match.group(1)
        else_value = match.group(2)

    for entity in entities:
        if entity['expr'] == then_value: return entity['name']
        if entity['expr'] == else_value: return entity['name']
