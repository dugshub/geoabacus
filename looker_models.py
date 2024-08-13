import lkml

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
    agg = metric.measures[0]['agg']
    metric = {"measure":
        {
            "type": convert_metric_type(metric),
            "label": metric.label,
            "description": metric.description or "",
            "sql": f"${{TABLE}}.{metric.name}",
            "name": metric.name,

        }
    }
    #
    return lkml.dump(metric)


def convert_metric_type(dimension):
    if dimension.type == 'CATEGORICAL':
        return 'sum'

    else:
        return 'sum_distinct'
    #  sql_distinct_key: ${order_id} ;;

    if dimension.type == 'CATEGORICAL':
        return 'count'

    if dimension.type == 'CATEGORICAL':
        return 'count_distinct'
    #  sql_distinct_key: ${order_id} ;;

    else:
        return 'number'
