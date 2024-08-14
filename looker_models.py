import lkml
import re

from app.models import Dimension, Metric


def to_looker_dimension(dimension: Dimension):
    dim = {"dimension":
        {
            "type": convert_type(dimension),
            "label": dimension.label,
            "description": dimension.description or "",
            "sql": f"${{TABLE}}.{dimension.name}",
            "name": dimension.name

        }
    }

    return lkml.dump(dim)


def convert_type(dimension):
    if dimension.type == 'CATEGORICAL':
        return 'string'

    else:
        return 'date'


def to_looker_measure(metric: Metric):
    # currently only works for metrics based off one measure
    lookml_metric = {"measure":
        {
            "label": metric.label,
            "description": metric.description or "",
            "sql": f"${{TABLE}}.{metric.name}",
            "name": metric.name,

        }
    }
    properties = convert_metric_type(metric)
    [lookml_metric['measure'].update(property) for property in properties]

    return lkml.dump(lookml_metric)


def convert_metric_type(metric):
    properties = []

    agg = metric.measures[0]['agg']

    if metric.type == 'SIMPLE':
        if agg == "SUM" or agg == "COUNT":
            properties.append({"type": agg.lower()})


        elif agg == "COUNT_DISTINCT":
            properties.append({"type": "count_distinct"})
            properties.append({"sql_distinct_key": _get_distinct_identity(metric)})

        elif agg == "SUM_DISTINCT":
            properties.append({"type": "sum_distinct"})
            properties.append({"sql_distinct_key": _get_distinct_identity(metric)})

        elif agg == "AVG":
            return "havent built this yet"

    elif metric.type == "DERIVED":
        pass

    elif metric.type == "RATIO":
        pass

    return properties

def _get_distinct_identity(metric):
    sql_string = metric.measures[0]['expr']
    pattern = r'CASE\s+WHEN\s+\S+\s+THEN\s+(\S+)\s+ELSE\s+(\S+)\s+END'

    # Search for the pattern in the input string
    match = re.search(pattern, sql_string, re.IGNORECASE)

    if match:
        then_value = match.group(1)
        else_value = match.group(2)

        # Define what counts as a non-field value
        non_field_values = {'NULL', '0', ''}

        # Return the valid field value, prioritizing THEN value if both are valid
        if then_value not in non_field_values:
            return then_value
        elif else_value not in non_field_values:
            return else_value
        else:
            return None
    else:
        return None
