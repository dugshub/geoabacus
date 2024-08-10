
view: rental_performance_2 {
    derived_table: {
        sql: select * from dbt_looker.rental_performance  ;;
        sql_trigger_value: SELECT FLOOR(((TIMESTAMP_DIFF(CURRENT_TIMESTAMP(),'1970-01-01 00:00:00',SECOND)) - 60*60*10)/(60*60*24));;
        sortkeys: ["metric_time__day"]

    }

    measure: gov_local{
        label: "GOV Local"
        description: "The sum of checkout price including all fees. This only accounts rentals with 'payment_status' = 'success' and 'reservation_status' = 'valid'"
        type: sum
        sql: ${TABLE}.gov_local;;
        view_label: "   Metrics"
        group_label: "Operational Financial Metrics"
   }

    measure: remittable_fee_revenue_local{
        label: "Remittable Fee Revenue Local"
        description: "The sum of fees collected that are included in the Display Price. This only accounts rentals with 'payment_status' = 'success' and 'reservation_status' = 'valid'.  Note: This metric is included within the GMV metric. If this is selected alongside GMV  you will be double counting revenue.      "
        type: sum
        sql: ${TABLE}.remittable_fee_revenue_local;;
        view_label: "   Metrics"
        group_label: "Operational Financial Metrics"
   }

    measure: rental_remit_local{
        label: "Rental Remit Local"
        description: "The total value remitted to the operator from valid rentals."
        type: sum
        sql: ${TABLE}.rental_remit_local;;
        view_label: "   Metrics"
        group_label: "Operational Financial Metrics"
   }

    measure: rentals_sold{
        label: "Rentals Sold"
        description: "Count of rentals created where payment status is 'success' and reservation status is 'valid'."
        type: sum
        sql: ${TABLE}.rentals_sold;;
        view_label: "   Metrics"
        group_label: "Rental Counts"
   }

    measure: rentals_ending{
        label: "Rentals Ending"
        description: "Count of rentals ending where payment status is 'success' and reservation status is 'valid'."
        type: sum
        sql: ${TABLE}.rentals_ending;;
        view_label: "   Metrics"
        group_label: "Rental Counts"
   }

    measure: rentals_starting{
        label: "Rentals Starting"
        description: "Count of rentals starting where payment status is 'success' and reservation status is 'valid'."
        type: sum
        sql: ${TABLE}.rentals_starting;;
        view_label: "   Metrics"
        group_label: "Rental Counts"
   }

    measure: facilities_with_rentals_sold{
        label: "Facilities With Rental Sold"
        description: "Distinct count of facilities with a rental sold where payment status is 'success' and reservation status is 'valid'."
        type: sum
        sql: ${TABLE}.facilities_with_rentals_sold;;
        view_label: "   Metrics"
        group_label: "Facility Counts"
   }

    measure: facilities_with_rentals_ending{
        label: "Facilities With Rentals Ending"
        description: "Distinct count of facilities with rentals ending where payment status is 'success' and reservation status is 'valid'."
        type: sum
        sql: ${TABLE}.facilities_with_rentals_ending;;
        view_label: "   Metrics"
        group_label: "Facility Counts"
   }

    measure: facilities_with_rentals_starting{
        label: "Facilities With Rentals Starting"
        description: "Distinct count of facilities with rentals starting where payment status is 'success' and reservation status is 'valid'."
        type: sum
        sql: ${TABLE}.facilities_with_rentals_starting;;
        view_label: "   Metrics"
        group_label: "Facility Counts"
   }

    measure: renters_with_rentals_purchased{
        label: "Renters With A Purchase"
        description: "Distinct count of renters with a purchase where payment status is 'success' and reservation status is 'valid'."
        type: sum
        sql: ${TABLE}.renters_with_rentals_purchased;;
        view_label: "   Metrics"
        group_label: "Renter Counts"
   }

    measure: renters_with_rentals_ending{
        label: "Renters With Rentals Ending"
        description: "Distinct count of renters with rentals ending where payment status is 'success' and reservation status is 'valid'."
        type: sum
        sql: ${TABLE}.renters_with_rentals_ending;;
        view_label: "   Metrics"
        group_label: "Renter Counts"
   }

    measure: renters_with_rentals_starting{
        label: "Renters With Rentals Starting"
        description: "Distinct count of renters with rentals starting where payment status is 'success' and reservation status is 'valid'."
        type: sum
        sql: ${TABLE}.renters_with_rentals_starting;;
        view_label: "   Metrics"
        group_label: "Renter Counts"
   }

    dimension: event__created{
        label: "Created"
        description: "Creation date of the event."
        type: date
        sql: ${TABLE}.event__created;;
        view_label: "Events"
        group_label: "Date And Time"
   }

    dimension: event__deleted{
        label: "Deleted"
        description: "Indicates if the event is deleted."
        type: string
        sql: ${TABLE}.event__deleted;;
        view_label: "Events"
        group_label: "Date And Time"
   }

    dimension: event__description{
        label: "Description"
        description: "Description of the event."
        type: string
        sql: ${TABLE}.event__description;;
        view_label: "Events"

   }

    dimension: event__destination_id{
        label: "Destination ID"
        description: "Identifier for the associated destination."
        type: string
        sql: ${TABLE}.event__destination_id;;
        view_label: "Event Destination"
        group_label: "Id Fields"
   }

    dimension: event__ends{
        label: "Ends"
        description: "End date of the event."
        type: date
        sql: ${TABLE}.event__ends;;
        view_label: "Events"
        group_label: "Date And Time"
   }

    dimension: event__event_ends_offset{
        label: "Event Ends Offset"
        description: "Offset time when the event ends."
        type: string
        sql: ${TABLE}.event__event_ends_offset;;
        view_label: "Events"
        group_label: "Date And Time"
   }

    dimension: event__event_id{
        label: "Event ID"
        description: "Unique identifier for the event."
        type: string
        sql: ${TABLE}.event__event_id;;
        view_label: "Events"
        group_label: "Id Fields"
   }

    dimension: event__event_starts_offset{
        label: "Event Starts Offset"
        description: "Offset time when the event starts."
        type: string
        sql: ${TABLE}.event__event_starts_offset;;
        view_label: "Events"
        group_label: "Date And Time"
   }

    dimension: event__is_deleted_parent_event{
        label: "Is Deleted Parent Event"
        description: "Indicates if the parent event is deleted."
        type: string
        sql: ${TABLE}.event__is_deleted_parent_event;;
        view_label: "Events"

   }

    dimension: event__is_high_profile{
        label: "Is High Profile"
        description: "Indicates if the event is high profile."
        type: string
        sql: ${TABLE}.event__is_high_profile;;
        view_label: "Events"

   }

    dimension: event__last_updated{
        label: "Last Updated"
        description: "Last updated date of the event."
        type: date
        sql: ${TABLE}.event__last_updated;;
        view_label: "Events"

   }

    dimension: event__parent_event_id{
        label: "Parent Event ID"
        description: "Identifier for the parent event."
        type: string
        sql: ${TABLE}.event__parent_event_id;;
        view_label: "Events"
        group_label: "Id Fields"
   }

    dimension: event__popularity_score{
        label: "Popularity Score"
        description: "Popularity score of the event."
        type: string
        sql: ${TABLE}.event__popularity_score;;
        view_label: "Events"

   }

    dimension: event__seatgeek_destination{
        label: "SeatGeek Destination"
        description: "SeatGeek destination for the event."
        type: string
        sql: ${TABLE}.event__seatgeek_destination;;
        view_label: "Events"
        group_label: "Details"
   }

    dimension: event__seatgeek_id{
        label: "SeatGeek ID"
        description: "SeatGeek identifier for the event."
        type: string
        sql: ${TABLE}.event__seatgeek_id;;
        view_label: "Events"
        group_label: "Id Fields"
   }

    dimension: event__seatgeek_update{
        label: "SeatGeek Update"
        description: "Indicates if the event is updated in SeatGeek."
        type: string
        sql: ${TABLE}.event__seatgeek_update;;
        view_label: "Events"

   }

    dimension: event__short_description{
        label: "Short Description"
        description: "Short description of the event."
        type: string
        sql: ${TABLE}.event__short_description;;
        view_label: "Events"
        group_label: "Details"
   }

    dimension: event__starts{
        label: "Starts"
        description: "Start date of the event."
        type: date
        sql: ${TABLE}.event__starts;;
        view_label: "Events"
        group_label: "Date And Time"
   }

    dimension: event__title{
        label: "Title"
        description: "Title of the event."
        type: string
        sql: ${TABLE}.event__title;;
        view_label: "Events"
        group_label: "Details"
   }

    dimension: facility__account_owner{
        label: "Account Owner"
        description: "Account owner of the facility."
        type: string
        sql: ${TABLE}.facility__account_owner;;
        view_label: "Canonical Facility"
        group_label: "Facility Config Details"
   }

    dimension: facility__default_facility_spaces{
        label: "Default Facility Spaces"
        description: "Default number of spaces at the facility."
        type: string
        sql: ${TABLE}.facility__default_facility_spaces;;
        view_label: "Canonical Facility"
        group_label: "Facility Config Details"
   }

    dimension: facility__external_id{
        label: "External ID"
        description: "External identifier for the facility."
        type: string
        sql: ${TABLE}.facility__external_id;;
        view_label: "Canonical Facility"
        group_label: "Facility Config Details"
   }

    dimension: facility__facility_created_at{
        label: "Facility Created At"
        description: "Creation date of the facility."
        type: date
        sql: ${TABLE}.facility__facility_created_at;;
        view_label: "Canonical Facility"
        group_label: "Facility Config Details"
   }

    dimension: facility__facility_title{
        label: "Facility Title"
        description: "Title of the facility."
        type: string
        sql: ${TABLE}.facility__facility_title;;
        view_label: "Canonical Facility"
        group_label: "Facility Config Details"
   }

    dimension: facility__facility_type{
        label: "Facility Type"
        description: "Type of the facility."
        type: string
        sql: ${TABLE}.facility__facility_type;;
        view_label: "Canonical Facility"
        group_label: "Facility Config Details"
   }

    dimension: metric_time{
        label: "Metric Time"
        description: "Event time for metrics."
        type: date
        sql: ${TABLE}.metric_time__day;;
        view_label: "Date And Time"

   }

    dimension: rental__event_id{
        label: "Event ID"
        description: "Identifier for the event."
        type: string
        sql: ${TABLE}.rental__event_id;;
        view_label: "Rental"
        group_label: "Id Fields"
   }

    dimension: rental__facility_configuration_id{
        label: "Facility Configuration ID"
        description: "Identifier for the facility configuration."
        type: string
        sql: ${TABLE}.rental__facility_configuration_id;;
        view_label: "Rental"
        group_label: "Id Fields"
   }

    dimension: rental__is_valid{
        label: "Is Valid Rental"
        description: "Indicates if the rental is valid."
        type: string
        sql: ${TABLE}.rental__is_valid;;
        view_label: "Rental"
        group_label: "Reservation Details"
   }

    dimension: rental__partner_id{
        label: "Partner ID"
        description: "Identifier for the partner."
        type: string
        sql: ${TABLE}.rental__partner_id;;
        view_label: "Rental"
        group_label: "Id Fields"
   }

    dimension: rental__payment_type_title{
        label: "Payment Type Title"
        description: "Title of the payment type."
        type: string
        sql: ${TABLE}.rental__payment_type_title;;
        view_label: "Rental"
        group_label: "Rental Payment Details"
   }

    dimension: rental__rental_created_at_cst{
        label: "Rental Created At - CST"
        description: "Creation date of the rental in CST."
        type: date
        sql: ${TABLE}.rental__rental_created_at_cst;;
        view_label: "Date And Time"
        group_label: "Rental"
   }

    dimension: rental__rental_ends_at_local{
        label: "Rental Ends At - Local"
        description: "End date of the rental in local time."
        type: date
        sql: ${TABLE}.rental__rental_ends_at_local;;
        view_label: "Date And Time"
        group_label: "Rental"
   }

    dimension: rental__rental_ends_at_local_time{
        label: "Rental Ends At - Local Time"
        description: "End time of the rental in local time."
        type: string
        sql: ${TABLE}.rental__rental_ends_at_local_time;;
        view_label: "Date And Time"
        group_label: "Rental"
   }

    dimension: rental__rental_id{
        label: "Rental ID"
        description: "Unique identifier for the rental."
        type: string
        sql: ${TABLE}.rental__rental_id;;
        view_label: "Rental"
        group_label: "Id Fields"
   }

    dimension: rental__rental_lead_time_local{
        label: "Rental Lead Time - Local"
        description: "Lead time for the rental in local time."
        type: string
        sql: ${TABLE}.rental__rental_lead_time_local;;
        view_label: "Rental"
        group_label: "Lead Time"
   }

    dimension: rental__rental_length_hours{
        label: "Rental Length Hours"
        description: "Length of the rental in hours."
        type: string
        sql: ${TABLE}.rental__rental_length_hours;;
        view_label: "Rental"
        group_label: "Rental Length"
   }

    dimension: rental__rental_length_minutes{
        label: "Rental Length Minutes"
        description: "Length of the rental in minutes."
        type: string
        sql: ${TABLE}.rental__rental_length_minutes;;
        view_label: "Rental"
        group_label: "Rental Length"
   }

    dimension: rental__rental_payment_status{
        label: "Rental Payment Status"
        description: "Payment status of the rental."
        type: string
        sql: ${TABLE}.rental__rental_payment_status;;
        view_label: "Rental"
        group_label: "Rental Payment Details"
   }

    dimension: rental__rental_reservation_status{
        label: "Rental Reservation Status"
        description: "Reservation status of the rental."
        type: string
        sql: ${TABLE}.rental__rental_reservation_status;;
        view_label: "Rental"
        group_label: "Reservation Details"
   }

    dimension: rental__rental_rule_type_title{
        label: "Rental Rule Type Title"
        description: "Rule type title for the rental."
        type: string
        sql: ${TABLE}.rental__rental_rule_type_title;;
        view_label: "Rental"
        group_label: "Reservation Details"
   }

    dimension: rental__rental_segment{
        label: "Rental Segment"
        description: "Segment of the rental."
        type: string
        sql: ${TABLE}.rental__rental_segment;;
        view_label: "Rental"
        group_label: "Rental Segmentation"
   }

    dimension: rental__rental_segment_rollup{
        label: "Rental Segment Rollup"
        description: "Rollup segment of the rental."
        type: string
        sql: ${TABLE}.rental__rental_segment_rollup;;
        view_label: "Rental"
        group_label: "Rental Segmentation"
   }

    dimension: rental__rental_source_title{
        label: "Rental Source Title"
        description: "Source title of the rental."
        type: string
        sql: ${TABLE}.rental__rental_source_title;;
        view_label: "Rental"
        group_label: "Reservation Details"
   }

    dimension: rental__rental_starts_at_local{
        label: "Rental Starts At - Local"
        description: "Start date of the rental in local time."
        type: date
        sql: ${TABLE}.rental__rental_starts_at_local;;
        view_label: "Date And Time"
        group_label: "Rental"
   }

    dimension: rental__rental_starts_at_local_time{
        label: "Rental Starts At - Local Time"
        description: "Start time of the rental in local time."
        type: string
        sql: ${TABLE}.rental__rental_starts_at_local_time;;
        view_label: "Date And Time"
        group_label: "Rental"
   }

    dimension: rental__renter_id{
        label: "Renter ID"
        description: "Identifier for the renter."
        type: string
        sql: ${TABLE}.rental__renter_id;;
        view_label: "Rental"
        group_label: "Id Fields"
   }

    dimension: renter__date_joined{
        label: "Date Joined"
        description: "Date when the renter joined."
        type: date
        sql: ${TABLE}.renter__date_joined;;
        view_label: "Renter Details"
        group_label: "Signup And Recency"
   }

    dimension: renter__days_since_first_rental{
        label: "Days Since First Rental"
        description: "Number of days since the renter's first rental."
        type: string
        sql: ${TABLE}.renter__days_since_first_rental;;
        view_label: "Renter Details"
        group_label: "Signup And Recency"
   }

    dimension: renter__days_since_last_rental{
        label: "Days Since Last Rental"
        description: "Number of days since the renter's last rental."
        type: string
        sql: ${TABLE}.renter__days_since_last_rental;;
        view_label: "Renter Details"
        group_label: "Signup And Recency"
   }

    dimension: renter__email{
        label: "Email"
        description: "Email address of the renter."
        type: string
        sql: ${TABLE}.renter__email;;
        view_label: "Renter Details"
        group_label: "Details"
   }

    dimension: renter__first_name{
        label: "First Name"
        description: "First name of the renter."
        type: string
        sql: ${TABLE}.renter__first_name;;
        view_label: "Renter Details"
        group_label: "Details"
   }

    dimension: renter__first_rental_date{
        label: "First Rental Date"
        description: "Date of the renter's first rental."
        type: date
        sql: ${TABLE}.renter__first_rental_date;;
        view_label: "Renter Details"
        group_label: "Signup And Recency"
   }

    dimension: renter__first_rental_id{
        label: "First Rental ID"
        description: "Identifier for the renter's first rental."
        type: string
        sql: ${TABLE}.renter__first_rental_id;;
        view_label: "Renter Details"
        group_label: "Id Fields"
   }

    dimension: renter__last_name{
        label: "Last Name"
        description: "Last name of the renter."
        type: string
        sql: ${TABLE}.renter__last_name;;
        view_label: "Renter Details"
        group_label: "Details"
   }

    dimension: renter__last_rental_date{
        label: "Last Rental Date"
        description: "Date of the renter's last rental."
        type: date
        sql: ${TABLE}.renter__last_rental_date;;
        view_label: "Renter Details"
        group_label: "Signup And Recency"
   }

    dimension: renter__last_rental_id{
        label: "Last Rental ID"
        description: "Identifier for the renter's last rental."
        type: string
        sql: ${TABLE}.renter__last_rental_id;;
        view_label: "Renter Details"
        group_label: "Id Fields"
   }

    dimension: renter__lifetime_rentals{
        label: "Lifetime Rentals"
        description: "Total number of rentals by the renter."
        type: string
        sql: ${TABLE}.renter__lifetime_rentals;;
        view_label: "Renter Details"

   }

    dimension: renter__lifetime_value{
        label: "Lifetime Value"
        description: "Total value of rentals by the renter."
        type: string
        sql: ${TABLE}.renter__lifetime_value;;
        view_label: "Renter Details"

   }

    dimension: renter__phone_number{
        label: "Phone Number"
        description: "Phone number of the renter."
        type: string
        sql: ${TABLE}.renter__phone_number;;
        view_label: "Renter Details"
        group_label: "Details"
   }

    dimension: renter__renter_id{
        label: "Renter ID"
        description: "Unique identifier for the renter."
        type: string
        sql: ${TABLE}.renter__renter_id;;
        view_label: "Renter Details"
        group_label: "Id Fields"
   }
}