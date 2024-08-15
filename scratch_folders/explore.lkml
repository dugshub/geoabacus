view: rental_performance {
  derived_table: {
    sql: select * from dbt_looker.rental_performance ;;
    sql_trigger_value: SELECT FLOOR(((TIMESTAMP_DIFF(CURRENT_TIMESTAMP(),'1970-01-01 00:00:00',SECOND)) - 60*60*10)/(60*60*24)) ;;
  }

  measure: remittable_fee_revenue_local {
    label: "Remittable Fee Revenue Local"
    description: "The sum of fees collected that are included in the Display Price. This only accounts rentals with 'payment_status' = 'success' and 'reservation_status' = 'valid'.  Note: This metric is included within the GMV metric. If this is selected alongside GMV  you will be double counting revenue.      "
    sql: ${TABLE}.remittable_fee_revenue_local ;;
    type: sum
  }

  measure: renters_with_rentals_ending {
    label: "Renters With Rentals Ending"
    description: "Distinct count of renters with at least one rental ending where payment status is 'success' and reservation status is 'valid'."
    sql: ${TABLE}.renters_with_rentals_ending ;;
    type: count_distinct
    sql_distinct_key: ${renter} ;;
  }

  dimension: renter__lifetime_credit_used {
    type: string
    label: "Lifetime Credit Used"
    description: "Total credit used by the renter."
    sql: ${TABLE}.renter__lifetime_credit_used ;;
  }

  dimension: renter__days_since_first_rental {
    type: string
    label: "Days Since First Rental"
    description: "Number of days since the renter's first rental."
    sql: ${TABLE}.renter__days_since_first_rental ;;
  }
}