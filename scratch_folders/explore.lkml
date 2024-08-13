measure: gov_local {
  type: sum_distinct
  label: "GOV Local"
  description: "The sum of checkout price including all fees. This only accounts rentals with 'payment_status' = 'success' and 'reservation_status' = 'valid'"
  sql: ${TABLE}.gov_local ;;
}
measure: remittable_fee_revenue_local {
  type: sum_distinct
  label: "Remittable Fee Revenue Local"
  description: "The sum of fees collected that are included in the Display Price. This only accounts rentals with 'payment_status' = 'success' and 'reservation_status' = 'valid'.  Note: This metric is included within the GMV metric. If this is selected alongside GMV  you will be double counting revenue.      "
  sql: ${TABLE}.remittable_fee_revenue_local ;;
}
measure: rental_remit_local {
  type: sum_distinct
  label: "Rental Remit Local"
  description: "The total value remitted to the operator from valid rentals."
  sql: ${TABLE}.rental_remit_local ;;
}
measure: rentals_sold {
  type: sum_distinct
  label: "Rentals Sold"
  description: "Count of rentals created where payment status is 'success' and reservation status is 'valid'."
  sql: ${TABLE}.rentals_sold ;;
}
measure: rentals_ending {
  type: sum_distinct
  label: "Rentals Ending"
  description: "Count of rentals ending where payment status is 'success' and reservation status is 'valid'."
  sql: ${TABLE}.rentals_ending ;;
}
measure: rentals_starting {
  type: sum_distinct
  label: "Rentals Starting"
  description: "Count of rentals starting where payment status is 'success' and reservation status is 'valid'."
  sql: ${TABLE}.rentals_starting ;;
}
measure: facilities_with_rentals_sold {
  type: sum_distinct
  label: "Facilities With Rentals Sold"
  description: "Distinct count of facilities with a rental sold where payment status is 'success' and reservation status is 'valid'."
  sql: ${TABLE}.facilities_with_rentals_sold ;;
}
measure: facilities_with_rentals_ending {
  type: sum_distinct
  label: "Facilities With Rentals Ending"
  description: "Distinct count of facilities with rentals ending where payment status is 'success' and reservation status is 'valid'."
  sql: ${TABLE}.facilities_with_rentals_ending ;;
}
measure: facilities_with_rentals_starting {
  type: sum_distinct
  label: "Facilities With Rentals Starting"
  description: "Distinct count of facilities with rentals starting where payment status is 'success' and reservation status is 'valid'."
  sql: ${TABLE}.facilities_with_rentals_starting ;;
}
measure: renters_with_rentals_purchased {
  type: sum_distinct
  label: "Renters With A Purchase"
  description: "Distinct count of renters with at least one purchase where payment status is 'success' and reservation status is 'valid'."
  sql: ${TABLE}.renters_with_rentals_purchased ;;
}
measure: renters_with_rentals_ending {
  type: sum_distinct
  label: "Renters With Rentals Ending"
  description: "Distinct count of renters with at least one rental ending where payment status is 'success' and reservation status is 'valid'."
  sql: ${TABLE}.renters_with_rentals_ending ;;
}
measure: renters_with_rentals_starting {
  type: sum_distinct
  label: "Renters With Rentals Starting"
  description: "Distinct count of renters with at least one rental starting where payment status is 'success' and reservation status is 'valid'."
  sql: ${TABLE}.renters_with_rentals_starting ;;
}
}