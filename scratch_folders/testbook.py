data = \
  { "metrics": [
    {
      "name": "gov_local",
      "label": "GOV Local",
      "description": "The sum of checkout price including all fees. This only accounts rentals with 'payment_status' = 'success' and 'reservation_status' = 'valid'",
      "type": "SIMPLE",
      "config": {
        "meta": {
          "group": "Core",
          "metric_type": "Operational Financial Metrics",
          "metric_category": "Financial Metrics"
        }
      }
    },
    {
      "name": "remittable_fee_revenue_local",
      "label": "Remittable Fee Revenue Local",
      "description": "The sum of fees collected that are included in the Display Price. This only accounts rentals with 'payment_status' = 'success' and 'reservation_status' = 'valid'.  Note: This metric is included within the GMV metric. If this is selected alongside GMV  you will be double counting revenue.      ",
      "type": "SIMPLE",
      "config": {
        "meta": {
          "group": "Core",
          "metric_type": "Operational Financial Metrics",
          "metric_category": "Financial Metrics"
        }
      }
    },
    {
      "name": "rental_remit_local",
      "label": "Rental Remit Local",
      "description": "The total value remitted to the operator from valid rentals.",
      "type": "SIMPLE",
      "config": {
        "meta": {
          "group": "Core",
          "metric_type": "Operational Financial Metrics",
          "metric_category": "Financial Metrics"
        }
      }
    },
    {
      "name": "rentals_sold",
      "label": "Rentals Sold",
      "description": "Count of rentals created where payment status is 'success' and reservation status is 'valid'.",
      "type": "SIMPLE",
      "config": {
        "meta": {
          "group": "Core",
          "metric_type": "Rental Counts",
          "metric_category": "Count"
        }
      }
    },
    {
      "name": "rentals_ending",
      "label": "Rentals Ending",
      "description": "Count of rentals ending where payment status is 'success' and reservation status is 'valid'.",
      "type": "SIMPLE",
      "config": {
        "meta": {
          "group": "Core",
          "metric_type": "Rental Counts",
          "metric_category": "Count"
        }
      }
    },
    {
      "name": "rentals_starting",
      "label": "Rentals Starting",
      "description": "Count of rentals starting where payment status is 'success' and reservation status is 'valid'.",
      "type": "SIMPLE",
      "config": {
        "meta": {
          "group": "Core",
          "metric_type": "Rental Counts",
          "metric_category": "Count"
        }
      }
    },
    {
      "name": "facilities_with_rentals_sold",
      "label": "Facilities With Rentals Sold",
      "description": "Distinct count of facilities with a rental sold where payment status is 'success' and reservation status is 'valid'.",
      "type": "SIMPLE",
      "config": {
        "meta": {
          "group": "Core",
          "metric_type": "Facility Counts",
          "metric_category": "Count"
        }
      }
    },
    {
      "name": "facilities_with_rentals_ending",
      "label": "Facilities With Rentals Ending",
      "description": "Distinct count of facilities with rentals ending where payment status is 'success' and reservation status is 'valid'.",
      "type": "SIMPLE",
      "config": {
        "meta": {
          "group": "Core",
          "metric_type": "Facility Counts",
          "metric_category": "Count"
        }
      }
    },
    {
      "name": "facilities_with_rentals_starting",
      "label": "Facilities With Rentals Starting",
      "description": "Distinct count of facilities with rentals starting where payment status is 'success' and reservation status is 'valid'.",
      "type": "SIMPLE",
      "config": {
        "meta": {
          "group": "Core",
          "metric_type": "Facility Counts",
          "metric_category": "Count"
        }
      }
    },
    {
      "name": "renters_with_rentals_purchased",
      "label": "Renters With A Purchase",
      "description": "Distinct count of renters with at least one purchase where payment status is 'success' and reservation status is 'valid'.",
      "type": "SIMPLE",
      "config": {
        "meta": {
          "group": "Core",
          "metric_type": "Renter Counts",
          "metric_category": "Count"
        }
      }
    },
    {
      "name": "renters_with_rentals_ending",
      "label": "Renters With Rentals Ending",
      "description": "Distinct count of renters with at least one rental ending where payment status is 'success' and reservation status is 'valid'.",
      "type": "SIMPLE",
      "config": {
        "meta": {
          "group": "Core",
          "metric_type": "Renter Counts",
          "metric_category": "Count"
        }
      }
    },
    {
      "name": "renters_with_rentals_starting",
      "label": "Renters With Rentals Starting",
      "description": "Distinct count of renters with at least one rental starting where payment status is 'success' and reservation status is 'valid'.",
      "type": "SIMPLE",
      "config": {
        "meta": {
          "group": "Core",
          "metric_type": "Renter Counts",
          "metric_category": "Count"
        }
      }
    }
  ]
}
metrics = data.get('metrics')
from app import app, db
from app.models import Metric,MetricTags,metrics_schema
with app.app_context():
  with db.session.no_autoflush:
    metrics = metrics_schema.load(metrics, session=db.session)

