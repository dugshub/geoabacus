view: rental_performance {
  derived_table: {
    sql: select * from dbt_looker.rental_performance ;;
    sql_trigger_value: SELECT FLOOR(((TIMESTAMP_DIFF(CURRENT_TIMESTAMP(),'1970-01-01 00:00:00',SECOND)) - 60*60*10)/(60*60*24)) ;;
  }

  measure: gov_local {
    label: "GOV Local"
    description: "The sum of checkout price including all fees. This only accounts rentals with 'payment_status' = 'success' and 'reservation_status' = 'valid'"
    sql: ${TABLE}.gov_local ;;
    type: sum
  }

  measure: remittable_fee_revenue_local {
    label: "Remittable Fee Revenue Local"
    description: "The sum of fees collected that are included in the Display Price. This only accounts rentals with 'payment_status' = 'success' and 'reservation_status' = 'valid'.  Note: This metric is included within the GMV metric. If this is selected alongside GMV  you will be double counting revenue.      "
    sql: ${TABLE}.remittable_fee_revenue_local ;;
    type: sum
  }

  measure: rental_remit_local {
    label: "Rental Remit Local"
    description: "The total value remitted to the operator from valid rentals."
    sql: ${TABLE}.rental_remit_local ;;
    type: sum
  }

  measure: rentals_sold {
    label: "Rentals Sold"
    description: "Count of rentals created where payment status is 'success' and reservation status is 'valid'."
    sql: ${TABLE}.rentals_sold ;;
    type: sum
  }

  measure: rentals_ending {
    label: "Rentals Ending"
    description: "Count of rentals ending where payment status is 'success' and reservation status is 'valid'."
    sql: ${TABLE}.rentals_ending ;;
    type: sum
  }

  measure: rentals_starting {
    label: "Rentals Starting"
    description: "Count of rentals starting where payment status is 'success' and reservation status is 'valid'."
    sql: ${TABLE}.rentals_starting ;;
    type: sum
  }

  measure: facilities_with_rentals_sold {
    label: "Facilities With Rentals Sold"
    description: "Distinct count of facilities with a rental sold where payment status is 'success' and reservation status is 'valid'."
    sql: ${TABLE}.facilities_with_rentals_sold ;;
    type: SUM_DISTINCT
    sql_distinct_key: ${facility} ;;
  }

  measure: facilities_with_rentals_ending {
    label: "Facilities With Rentals Ending"
    description: "Distinct count of facilities with rentals ending where payment status is 'success' and reservation status is 'valid'."
    sql: ${TABLE}.facilities_with_rentals_ending ;;
    type: SUM_DISTINCT
    sql_distinct_key: ${facility} ;;
  }

  measure: facilities_with_rentals_starting {
    label: "Facilities With Rentals Starting"
    description: "Distinct count of facilities with rentals starting where payment status is 'success' and reservation status is 'valid'."
    sql: ${TABLE}.facilities_with_rentals_starting ;;
    type: SUM_DISTINCT
    sql_distinct_key: ${facility} ;;
  }

  measure: renters_with_rentals_purchased {
    label: "Renters With A Purchase"
    description: "Distinct count of renters with at least one purchase where payment status is 'success' and reservation status is 'valid'."
    sql: ${TABLE}.renters_with_rentals_purchased ;;
    type: SUM_DISTINCT
    sql_distinct_key: ${renter} ;;
  }

  measure: renters_with_rentals_ending {
    label: "Renters With Rentals Ending"
    description: "Distinct count of renters with at least one rental ending where payment status is 'success' and reservation status is 'valid'."
    sql: ${TABLE}.renters_with_rentals_ending ;;
    type: SUM_DISTINCT
    sql_distinct_key: ${renter} ;;
  }

  measure: renters_with_rentals_starting {
    label: "Renters With Rentals Starting"
    description: "Distinct count of renters with at least one rental starting where payment status is 'success' and reservation status is 'valid'."
    sql: ${TABLE}.renters_with_rentals_starting ;;
    type: SUM_DISTINCT
    sql_distinct_key: ${renter} ;;
  }

  dimension: renter__lifetime_credit_used {
    type: string
    label: "Lifetime Credit Used"
    description: "Total credit used by the renter."
    sql: ${TABLE}.renter__lifetime_credit_used ;;
  }

  dimension: renter__lifetime_rentals {
    type: string
    label: "Lifetime Rentals"
    description: "Total number of rentals by the renter."
    sql: ${TABLE}.renter__lifetime_rentals ;;
  }

  dimension: renter__lifetime_value {
    type: string
    label: "Lifetime Value"
    description: "Total value of rentals by the renter."
    sql: ${TABLE}.renter__lifetime_value ;;
  }

  dimension: renter__email {
    type: string
    label: "Email"
    description: "Email address of the renter."
    sql: ${TABLE}.renter__email ;;
  }

  dimension: renter__first_name {
    type: string
    label: "First Name"
    description: "First name of the renter."
    sql: ${TABLE}.renter__first_name ;;
  }

  dimension: renter__last_name {
    type: string
    label: "Last Name"
    description: "Last name of the renter."
    sql: ${TABLE}.renter__last_name ;;
  }

  dimension: renter__phone_number {
    type: string
    label: "Phone Number"
    description: "Phone number of the renter."
    sql: ${TABLE}.renter__phone_number ;;
  }

  dimension: renter__first_rental_id {
    type: string
    label: "First Rental ID"
    description: "Identifier for the renter's first rental."
    sql: ${TABLE}.renter__first_rental_id ;;
  }

  dimension: renter__last_rental_id {
    type: string
    label: "Last Rental ID"
    description: "Identifier for the renter's last rental."
    sql: ${TABLE}.renter__last_rental_id ;;
  }

  dimension: renter__renter_id {
    type: string
    label: "Renter ID"
    description: "Unique identifier for the renter."
    sql: ${TABLE}.renter__renter_id ;;
  }

  dimension: renter__date_joined {
    type: date
    label: "Date Joined"
    description: "Date when the renter joined."
    sql: ${TABLE}.renter__date_joined ;;
  }

  dimension: renter__days_since_first_rental {
    type: string
    label: "Days Since First Rental"
    description: "Number of days since the renter's first rental."
    sql: ${TABLE}.renter__days_since_first_rental ;;
  }

  dimension: renter__days_since_last_rental {
    type: string
    label: "Days Since Last Rental"
    description: "Number of days since the renter's last rental."
    sql: ${TABLE}.renter__days_since_last_rental ;;
  }

  dimension: renter__first_rental_date {
    type: date
    label: "First Rental Date"
    description: "Date of the renter's first rental."
    sql: ${TABLE}.renter__first_rental_date ;;
  }

  dimension: renter__last_rental_date {
    type: date
    label: "Last Rental Date"
    description: "Date of the renter's last rental."
    sql: ${TABLE}.renter__last_rental_date ;;
  }

  dimension: rental__event_id {
    type: string
    label: "Event ID"
    description: "Identifier for the event."
    sql: ${TABLE}.rental__event_id ;;
  }

  dimension: rental__facility_configuration_id {
    type: string
    label: "Facility Configuration ID"
    description: "Identifier for the facility configuration."
    sql: ${TABLE}.rental__facility_configuration_id ;;
  }

  dimension: rental__partner_id {
    type: string
    label: "Partner ID"
    description: "Identifier for the partner."
    sql: ${TABLE}.rental__partner_id ;;
  }

  dimension: rental__rental_id {
    type: string
    label: "Rental ID"
    description: "Unique identifier for the rental."
    sql: ${TABLE}.rental__rental_id ;;
  }

  dimension: rental__renter_id {
    type: string
    label: "Renter ID"
    description: "Identifier for the renter."
    sql: ${TABLE}.rental__renter_id ;;
  }

  dimension: rental__rental_lead_time {
    type: string
    label: "Rental Lead Time"
    description: "Lead time for the rental in CST."
    sql: ${TABLE}.rental__rental_lead_time ;;
  }

  dimension: rental__rental_lead_time_local {
    type: string
    label: "Rental Lead Time - Local"
    description: "Lead time for the rental in local time."
    sql: ${TABLE}.rental__rental_lead_time_local ;;
  }

  dimension: rental__rental_length_hours {
    type: string
    label: "Rental Length Hours"
    description: "Length of the rental in hours."
    sql: ${TABLE}.rental__rental_length_hours ;;
  }

  dimension: rental__rental_length_minutes {
    type: string
    label: "Rental Length Minutes"
    description: "Length of the rental in minutes."
    sql: ${TABLE}.rental__rental_length_minutes ;;
  }

  dimension: rental__payment_type_title {
    type: string
    label: "Payment Type Title"
    description: "Title of the payment type."
    sql: ${TABLE}.rental__payment_type_title ;;
  }

  dimension: rental__rental_payment_status {
    type: string
    label: "Rental Payment Status"
    description: "Payment status of the rental."
    sql: ${TABLE}.rental__rental_payment_status ;;
  }

  dimension: rental__rental_payment_type_title {
    type: string
    label: "Rental Payment Type Title"
    description: "Payment type title for the rental."
    sql: ${TABLE}.rental__rental_payment_type_title ;;
  }

  dimension: rental__rental_segment {
    type: string
    label: "Rental Segment"
    description: "Segment of the rental."
    sql: ${TABLE}.rental__rental_segment ;;
  }

  dimension: rental__rental_segment_rollup {
    type: string
    label: "Rental Segment Rollup"
    description: "Rollup segment of the rental."
    sql: ${TABLE}.rental__rental_segment_rollup ;;
  }

  dimension: rental__is_valid {
    type: string
    label: "Is Valid Rental"
    description: "Indicates if the rental is valid."
    sql: ${TABLE}.rental__is_valid ;;
  }

  dimension: rental__rental_reservation_status {
    type: string
    label: "Rental Reservation Status"
    description: "Reservation status of the rental."
    sql: ${TABLE}.rental__rental_reservation_status ;;
  }

  dimension: rental__rental_rule_type_title {
    type: string
    label: "Rental Rule Type Title"
    description: "Rule type title for the rental."
    sql: ${TABLE}.rental__rental_rule_type_title ;;
  }

  dimension: rental__rental_source_title {
    type: string
    label: "Rental Source Title"
    description: "Source title of the rental."
    sql: ${TABLE}.rental__rental_source_title ;;
  }

  dimension: facility__geography__country_name {
    type: string
    label: "Country Name"
    description: "Name of the country."
    sql: ${TABLE}.facility__geography__country_name ;;
  }

  dimension: facility__geography__county_name {
    type: string
    label: "County Name"
    description: "Name of the county."
    sql: ${TABLE}.facility__geography__county_name ;;
  }

  dimension: facility__geography__locality_name {
    type: string
    label: "Locality Name"
    description: "Name of the locality."
    sql: ${TABLE}.facility__geography__locality_name ;;
  }

  dimension: facility__geography__neighbourhood_name {
    type: string
    label: "Neighbourhood Name"
    description: "Name of the neighbourhood."
    sql: ${TABLE}.facility__geography__neighbourhood_name ;;
  }

  dimension: facility__geography__region_name {
    type: string
    label: "Region Name"
    description: "Name of the region."
    sql: ${TABLE}.facility__geography__region_name ;;
  }

  dimension: facility__geography__geography_id {
    type: string
    label: "Geography ID"
    description: "Unique identifier for the geography."
    sql: ${TABLE}.facility__geography__geography_id ;;
  }

  dimension: facility__canonical_facility__reporting_market {
    type: string
    label: "Reporting Market"
    description: "Reporting market of the canonical facility."
    sql: ${TABLE}.facility__canonical_facility__reporting_market ;;
  }

  dimension: facility__canonical_facility__reporting_market_top_6_canada {
    type: string
    label: "Reporting Market Top 6 Canada"
    description: "Indicates if the facility is in the top 6 reporting markets in Canada."
    sql: ${TABLE}.facility__canonical_facility__reporting_market_top_6_canada ;;
  }

  dimension: facility__canonical_facility__reporting_market_top_8 {
    type: string
    label: "Reporting Market Top 8"
    description: "Indicates if the facility is in the top"
    sql: ${TABLE}.facility__canonical_facility__reporting_market_top_8 ;;
  }

  dimension: event__category {
    type: string
    label: "Category"
    description: "Category of the event."
    sql: ${TABLE}.event__category ;;
  }

  dimension: event__description {
    type: string
    label: "Description"
    description: "Description of the event."
    sql: ${TABLE}.event__description ;;
  }

  dimension: event__is_deleted_parent_event {
    type: string
    label: "Is Deleted Parent Event"
    description: "Indicates if the parent event is deleted."
    sql: ${TABLE}.event__is_deleted_parent_event ;;
  }

  dimension: event__is_high_profile {
    type: string
    label: "Is High Profile"
    description: "Indicates if the event is high profile."
    sql: ${TABLE}.event__is_high_profile ;;
  }

  dimension: event__last_updated {
    type: date
    label: "Last Updated"
    description: "Last updated date of the event."
    sql: ${TABLE}.event__last_updated ;;
  }

  dimension: event__popularity_score {
    type: string
    label: "Popularity Score"
    description: "Popularity score of the event."
    sql: ${TABLE}.event__popularity_score ;;
  }

  dimension: event__seatgeek_update {
    type: string
    label: "SeatGeek Update"
    description: "Indicates if the event is updated in SeatGeek."
    sql: ${TABLE}.event__seatgeek_update ;;
  }

  dimension: event__created {
    type: date
    label: "Created"
    description: "Creation date of the event."
    sql: ${TABLE}.event__created ;;
  }

  dimension: event__deleted {
    type: string
    label: "Deleted"
    description: "Indicates if the event is deleted."
    sql: ${TABLE}.event__deleted ;;
  }

  dimension: event__ends {
    type: date
    label: "Ends"
    description: "End date of the event."
    sql: ${TABLE}.event__ends ;;
  }

  dimension: event__event_ends_offset {
    type: string
    label: "Event Ends Offset"
    description: "Offset time when the event ends."
    sql: ${TABLE}.event__event_ends_offset ;;
  }

  dimension: event__event_starts_offset {
    type: string
    label: "Event Starts Offset"
    description: "Offset time when the event starts."
    sql: ${TABLE}.event__event_starts_offset ;;
  }

  dimension: event__starts {
    type: date
    label: "Starts"
    description: "Start date of the event."
    sql: ${TABLE}.event__starts ;;
  }

  dimension: event__seatgeek_destination {
    type: string
    label: "SeatGeek Destination"
    description: "SeatGeek destination for the event."
    sql: ${TABLE}.event__seatgeek_destination ;;
  }

  dimension: event__short_description {
    type: string
    label: "Short Description"
    description: "Short description of the event."
    sql: ${TABLE}.event__short_description ;;
  }

  dimension: event__title {
    type: string
    label: "Title"
    description: "Title of the event."
    sql: ${TABLE}.event__title ;;
  }

  dimension: event__event_id {
    type: string
    label: "Event ID"
    description: "Unique identifier for the event."
    sql: ${TABLE}.event__event_id ;;
  }

  dimension: event__parent_event_id {
    type: string
    label: "Parent Event ID"
    description: "Identifier for the parent event."
    sql: ${TABLE}.event__parent_event_id ;;
  }

  dimension: event__seatgeek_id {
    type: string
    label: "SeatGeek ID"
    description: "SeatGeek identifier for the event."
    sql: ${TABLE}.event__seatgeek_id ;;
  }

  dimension: event__destination__can_have_events {
    type: string
    label: "Can Have Events"
    description: "Indicates if the destination can have events."
    sql: ${TABLE}.event__destination__can_have_events ;;
  }

  dimension: event__destination__city {
    type: string
    label: "City"
    description: "City where the destination is located."
    sql: ${TABLE}.event__destination__city ;;
  }

  dimension: event__destination__default_event_length {
    type: string
    label: "Default Event Length"
    description: "Default event length for the destination."
    sql: ${TABLE}.event__destination__default_event_length ;;
  }

  dimension: event__destination__deleted {
    type: string
    label: "Deleted"
    description: "Indicates if the destination is deleted."
    sql: ${TABLE}.event__destination__deleted ;;
  }

  dimension: event__destination__description {
    type: string
    label: "Description"
    description: "Description of the destination."
    sql: ${TABLE}.event__destination__description ;;
  }

  dimension: event__destination__desktop_zoom_level {
    type: string
    label: "Desktop Zoom Level"
    description: "Desktop zoom level for the destination."
    sql: ${TABLE}.event__destination__desktop_zoom_level ;;
  }

  dimension: event__destination__hide_event_modal {
    type: string
    label: "Hide Event Modal"
    description: "Indicates if the event modal is hidden for the destination."
    sql: ${TABLE}.event__destination__hide_event_modal ;;
  }

  dimension: event__destination__last_updated {
    type: date
    label: "Last Updated"
    description: "Last updated date of the destination."
    sql: ${TABLE}.event__destination__last_updated ;;
  }

  dimension: event__destination__mobile_zoom_level {
    type: string
    label: "Mobile Zoom Level"
    description: "Mobile zoom level for the destination."
    sql: ${TABLE}.event__destination__mobile_zoom_level ;;
  }

  dimension: event__destination__monthly_enabled {
    type: string
    label: "Monthly Enabled"
    description: "Indicates if the destination is enabled monthly."
    sql: ${TABLE}.event__destination__monthly_enabled ;;
  }

  dimension: event__destination__override_ideal_zoom {
    type: string
    label: "Override Ideal Zoom"
    description: "Indicates if the ideal zoom level is overridden for the destination."
    sql: ${TABLE}.event__destination__override_ideal_zoom ;;
  }

  dimension: event__destination__seatgeek_auto_update {
    type: string
    label: "SeatGeek Auto Update"
    description: "Indicates if the destination is auto-updated in SeatGeek."
    sql: ${TABLE}.event__destination__seatgeek_auto_update ;;
  }

  dimension: event__destination__show_only_transient {
    type: string
    label: "Show Only Transient"
    description: "Indicates if only transient information is shown for the destination."
    sql: ${TABLE}.event__destination__show_only_transient ;;
  }

  dimension: event__destination__venue_content_enabled {
    type: string
    label: "Venue Content Enabled"
    description: "Indicates if venue content is enabled for the destination."
    sql: ${TABLE}.event__destination__venue_content_enabled ;;
  }

  dimension: event__destination__location_lat {
    type: string
    label: "Location Latitude"
    description: "Latitude of the destination's location."
    sql: ${TABLE}.event__destination__location_lat ;;
  }

  dimension: event__destination__location_lon {
    type: string
    label: "Location Longitude"
    description: "Longitude of the destination's location."
    sql: ${TABLE}.event__destination__location_lon ;;
  }

  dimension: event__destination__state {
    type: string
    label: "State"
    description: "State where the destination is located."
    sql: ${TABLE}.event__destination__state ;;
  }

  dimension: event__destination__street_address {
    type: string
    label: "Street Address"
    description: "Street address of the destination."
    sql: ${TABLE}.event__destination__street_address ;;
  }

  dimension: event__destination__zipcode {
    type: string
    label: "Zipcode"
    description: "Zip code of the destination."
    sql: ${TABLE}.event__destination__zipcode ;;
  }

  dimension: event__destination__created {
    type: date
    label: "Created"
    description: "Creation date of the destination."
    sql: ${TABLE}.event__destination__created ;;
  }

  dimension: event__destination__seatgeek_auto_create {
    type: string
    label: "SeatGeek Auto Create"
    description: "Indicates if the destination is auto-created in SeatGeek."
    sql: ${TABLE}.event__destination__seatgeek_auto_create ;;
  }

  dimension: event__destination__generic_destination {
    type: string
    label: "Generic Destination"
    description: "Indicates if the destination is generic."
    sql: ${TABLE}.event__destination__generic_destination ;;
  }

  dimension: event__destination__seatgeek_destination_title {
    type: string
    label: "SeatGeek Destination Title"
    description: "SeatGeek destination title for the destination."
    sql: ${TABLE}.event__destination__seatgeek_destination_title ;;
  }

  dimension: event__destination__status {
    type: string
    label: "Status"
    description: "Status of the destination."
    sql: ${TABLE}.event__destination__status ;;
  }

  dimension: event__destination__title {
    type: string
    label: "Title"
    description: "Title of the destination."
    sql: ${TABLE}.event__destination__title ;;
  }

  dimension: event__destination__destination_id {
    type: string
    label: "Destination ID"
    description: "Unique identifier for the destination."
    sql: ${TABLE}.event__destination__destination_id ;;
  }

  dimension: event__destination__parent_destination_id {
    type: string
    label: "Parent Destination ID"
    description: "Identifier for the parent destination."
    sql: ${TABLE}.event__destination__parent_destination_id ;;
  }

  dimension: event__destination__seatgeek_performer_id {
    type: string
    label: "SeatGeek Performer ID"
    description: "SeatGeek performer identifier for the destination."
    sql: ${TABLE}.event__destination__seatgeek_performer_id ;;
  }

  dimension: event__destination__spothero_city_id {
    type: string
    label: "SpotHero City ID"
    description: "SpotHero city identifier for the destination."
    sql: ${TABLE}.event__destination__spothero_city_id ;;
  }

  dimension: event__destination_id {
    type: string
    label: "Destination ID"
    description: "Identifier for the associated destination."
    sql: ${TABLE}.event__destination_id ;;
  }

  dimension: rental__rental_created_at_cst {
    type: date
    label: "Rental Created At - CST"
    description: "Creation date of the rental in CST."
    sql: ${TABLE}.rental__rental_created_at_cst ;;
  }

  dimension: rental__rental_created_at_local {
    type: date
    label: "Rental Created At - Local"
    description: "Creation date of the rental in local time."
    sql: ${TABLE}.rental__rental_created_at_local ;;
  }

  dimension: rental__rental_ends_at_cst {
    type: date
    label: "Rental Ends At - CST"
    description: "End date of the rental in CST."
    sql: ${TABLE}.rental__rental_ends_at_cst ;;
  }

  dimension: rental__rental_ends_at_cst_time {
    type: string
    label: "Rental Ends At - CST Time"
    description: "End time of the rental in CST."
    sql: ${TABLE}.rental__rental_ends_at_cst_time ;;
  }

  dimension: rental__rental_ends_at_local {
    type: date
    label: "Rental Ends At - Local"
    description: "End date of the rental in local time."
    sql: ${TABLE}.rental__rental_ends_at_local ;;
  }

  dimension: rental__rental_ends_at_local_time {
    type: string
    label: "Rental Ends At - Local Time"
    description: "End time of the rental in local time."
    sql: ${TABLE}.rental__rental_ends_at_local_time ;;
  }

  dimension: rental__rental_starts_at_cst {
    type: date
    label: "Rental Starts At - CST"
    description: "Start date of the rental in CST."
    sql: ${TABLE}.rental__rental_starts_at_cst ;;
  }

  dimension: rental__rental_starts_at_cst_time {
    type: string
    label: "Rental Starts At - CST Time"
    description: "Start time of the rental in CST."
    sql: ${TABLE}.rental__rental_starts_at_cst_time ;;
  }

  dimension: rental__rental_starts_at_local {
    type: date
    label: "Rental Starts At - Local"
    description: "Start date of the rental in local time."
    sql: ${TABLE}.rental__rental_starts_at_local ;;
  }

  dimension: rental__rental_starts_at_local_time {
    type: string
    label: "Rental Starts At - Local Time"
    description: "Start time of the rental in local time."
    sql: ${TABLE}.rental__rental_starts_at_local_time ;;
  }

  dimension: facility__canonical_facility__facility_currency {
    type: string
    label: "Facility Currency"
    description: "Currency used by the canonical facility."
    sql: ${TABLE}.facility__canonical_facility__facility_currency ;;
  }

  dimension: facility__canonical_facility__is_airport_facility {
    type: string
    label: "Is Airport Facility"
    description: "Indicates if the facility is an airport."
    sql: ${TABLE}.facility__canonical_facility__is_airport_facility ;;
  }

  dimension: facility__canonical_facility__address_id {
    type: string
    label: "Address ID"
    description: "Address identifier for the canonical facility."
    sql: ${TABLE}.facility__canonical_facility__address_id ;;
  }

  dimension: facility__canonical_facility__facility_timezone {
    type: string
    label: "Facility Timezone"
    description: "Timezone of the canonical facility."
    sql: ${TABLE}.facility__canonical_facility__facility_timezone ;;
  }

  dimension: facility__canonical_facility__canonical_facility_title {
    type: string
    label: "Canonical Facility Title"
    description: "Title of the canonical facility."
    sql: ${TABLE}.facility__canonical_facility__canonical_facility_title ;;
  }

  dimension: facility__account_owner {
    type: string
    label: "Account Owner"
    description: "Account owner of the facility."
    sql: ${TABLE}.facility__account_owner ;;
  }

  dimension: facility__default_facility_spaces {
    type: string
    label: "Default Facility Spaces"
    description: "Default number of spaces at the facility."
    sql: ${TABLE}.facility__default_facility_spaces ;;
  }

  dimension: facility__external_id {
    type: string
    label: "External ID"
    description: "External identifier for the facility."
    sql: ${TABLE}.facility__external_id ;;
  }

  dimension: facility__facility_created_at {
    type: date
    label: "Facility Created At"
    description: "Creation date of the facility."
    sql: ${TABLE}.facility__facility_created_at ;;
  }

  dimension: facility__facility_title {
    type: string
    label: "Facility Title"
    description: "Title of the facility."
    sql: ${TABLE}.facility__facility_title ;;
  }

  dimension: facility__facility_type {
    type: string
    label: "Facility Type"
    description: "Type of the facility."
    sql: ${TABLE}.facility__facility_type ;;
  }

  dimension: facility__canonical_facility__canonical_facility_id {
    type: string
    label: "Canonical Facility ID"
    description: "Unique identifier for the canonical facility."
    sql: ${TABLE}.facility__canonical_facility__canonical_facility_id ;;
  }

  dimension: facility__canonical_facility__external_id {
    type: string
    label: "External ID"
    description: "External identifier for the canonical facility."
    sql: ${TABLE}.facility__canonical_facility__external_id ;;
  }
}