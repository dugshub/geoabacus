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

  dimension: facility__canonical_facility__canonical_facility_id {
    type: stringre
    label: "Canonical Facility ID"
    description: "Unique identifier for the canonical facility.  This field corresponds to the ID in SpotHero Admin."
    sql: ${TABLE}.facility__canonical_facility__canonical_facility_id ;;
    view_label: "Canonical Facility"
  }

  dimension: facility__canonical_facility__canonical_facility_title {
    type: string
    label: "Canonical Facility Title"
    description: "Title of the canonical facility. This name will match what is provided in SpotHero Admin/SFDC."
    sql: ${TABLE}.facility__canonical_facility__canonical_facility_title ;;
    view_label: "Canonical Facility"
  }

  dimension: facility__canonical_facility__is_airport_facility {
    type: string
    label: "Is Airport Facility"
    description: "This field indicates if the facility is associated with an airport."
    sql: ${TABLE}.facility__canonical_facility__is_airport_facility ;;
    view_label: "Canonical Facility"
  }

  dimension: facility__default_facility_spaces {
    type: string
    label: "Default Facility Spaces"
    description: "Default number of spaces at the facility/parking spot. This can be set by SpotHero or the operator."
    sql: ${TABLE}.facility__default_facility_spaces ;;
    view_label: "Canonical Facility"
  }

  dimension: facility__facility_type {
    type: string
    label: "Facility Type"
    description: "Broad definition on the structure of the spot, such as 'lol', 'garage', or 'valet_stand'."
    sql: ${TABLE}.facility__facility_type ;;
    view_label: "Canonical Facility"
  }

  dimension: facility__facility_title {
    type: string
    label: "Facility Title"
    description: "Title of the facility/parking spot. This title will match the name in Admin as well as the SFDC opportunity."
    sql: ${TABLE}.facility__facility_title ;;
    view_label: "Canonical Facility"
  }

  dimension: facility__canonical_facility__address_id {
    type: string
    label: "Address ID"
    description: "Address identifier for the canonical facility.  This field relates the facility location to a specific address."
    sql: ${TABLE}.facility__canonical_facility__address_id ;;
    view_label: "Canonical Facility"
  }

  dimension: rental__rental_created_at_cst {
    type: date
    label: "Rental Created At - CST"
    description: "This field denotes the date of the rental purchase in CST. This date is pulled from a timestamp that is triggered upon receipt of the purchase in whichever medium the renter made the purchase."
    sql: ${TABLE}.rental__rental_created_at_cst ;;
    view_label: "Date and Time"
  }

  dimension: rental__rental_created_at_local {
    type: date
    label: "Rental Created At - Local"
    description: "This field denotes the date of the rental purchase in the time local to the facility attached to the rental. This date is pulled from a timestamp that is triggered upon receipt of the purchase in whichever medium the renter made the purchase."
    sql: ${TABLE}.rental__rental_created_at_local ;;
    view_label: "Date and Time"
  }

  dimension: rental__rental_ends_at_local {
    type: date
    label: "Rental Ends At - Local"
    description: "This field denotes the date the rental ends in the time local to the facility attached to the rental."
    sql: ${TABLE}.rental__rental_ends_at_local ;;
    view_label: "Date and Time"
  }

  dimension: rental__rental_starts_at_local {
    type: date
    label: "Rental Starts At - Local"
    description: "This field denotes the date the rental starts in the time local to the facility attached to the rental."
    sql: ${TABLE}.rental__rental_starts_at_local ;;
    view_label: "Date and Time"
  }

  dimension: event__destination__status {
    type: string
    label: "Status"
    description: "Destination/venue's status, where status corresponds to if the destination/venue is enabled/archived/deleted."
    sql: ${TABLE}.event__destination__status ;;
    view_label: "Event Destination"
  }

  dimension: event__destination__street_address {
    type: string
    label: "Street Address"
    description: "Street address of the destination/venue."
    sql: ${TABLE}.event__destination__street_address ;;
    view_label: "Event Destination"
  }

  dimension: event__destination__title {
    type: string
    label: "Title"
    description: "Title of the destination.  This is the title of the specific venue."
    sql: ${TABLE}.event__destination__title ;;
    view_label: "Event Destination"
  }

  dimension: event__destination__zipcode {
    type: string
    label: "Zipcode"
    description: "Zip code of the destination/venue."
    sql: ${TABLE}.event__destination__zipcode ;;
    view_label: "Event Destination"
  }

  dimension: event__destination__destination_id {
    type: string
    label: "Destination ID"
    description: "Unique identifier for the destination. A destination is attached to a specific venue (I.e. Staples Center/ Sofi)."
    sql: ${TABLE}.event__destination__destination_id ;;
    view_label: "Event Destination"
  }

  dimension: event__destination__description {
    type: string
    label: "Description"
    description: "A brief description of the venue. This can be anything from additional naming to a specific team/teams that play at this venue."
    sql: ${TABLE}.event__destination__description ;;
    view_label: "Event Destination"
  }

  dimension: event__event_id {
    type: string
    label: "Event ID"
    description: "This unique ID serves as the specific indentifier for a given event."
    sql: ${TABLE}.event__event_id ;;
    view_label: "Events"
  }

  dimension: event__is_high_profile {
    type: string
    label: "Is High Profile"
    description: "This field, pulled from monolith, denotes which events have a strict refund policy to dissuade resellers."
    sql: ${TABLE}.event__is_high_profile ;;
    view_label: "Events"
  }

  dimension: event__deleted {
    type: string
    label: "Deleted"
    description: "Indicates if the event is deleted out of SpotHero systems."
    sql: ${TABLE}.event__deleted ;;
    view_label: "Events"
  }

  dimension: event__ends {
    type: date
    label: "Ends"
    description: "End date of the event."
    sql: ${TABLE}.event__ends ;;
    view_label: "Events"
  }

  dimension: event__event_ends_offset {
    type: string
    label: "Event Ends Offset"
    description: "This field outlines the time buffer (in minutes) that is set up after the event ends during which event parking can end, as event rates can extend past the event end time"
    sql: ${TABLE}.event__event_ends_offset ;;
    view_label: "Events"
  }

  dimension: event__title {
    type: string
    label: "Title"
    description: "Title of the event."
    sql: ${TABLE}.event__title ;;
    view_label: "Events"
  }

  dimension: event__starts {
    type: date
    label: "Starts"
    description: "Start date of the event."
    sql: ${TABLE}.event__starts ;;
    view_label: "Events"
  }

  dimension: event__event_starts_offset {
    type: string
    label: "Event Starts Offset"
    description: "This field outlines the time buffer (in minutes) that is set up before the event starts during which event parking can begin, as event rates can beging before the event start time."
    sql: ${TABLE}.event__event_starts_offset ;;
    view_label: "Events"
  }

  dimension: event__parent_event_id {
    type: string
    label: "Parent Event ID"
    description: "This field serves as a rollup identifier for when multiple events are actually the same event (I.e. there is are 2 events for the same concert, but one is for the opener and one for the main act)."
    sql: ${TABLE}.event__parent_event_id ;;
    view_label: "Events"
  }

  dimension: event__seatgeek_id {
    type: string
    label: "SeatGeek ID"
    description: "This field is the associated identifier from an attached SeatGeek event."
    sql: ${TABLE}.event__seatgeek_id ;;
    view_label: "Events"
  }

  dimension: facility__geography__country_name {
    type: string
    label: "Country Name"
    description: "This field denotes the country the facility is in, I.e. USA or Canada."
    sql: ${TABLE}.facility__geography__country_name ;;
    view_label: "Geography"
  }

  dimension: facility__geography__county_name {
    type: string
    label: "County Name"
    description: "This field denotes the name of the county the facility is in, I.e. Cook or Hamilton."
    sql: ${TABLE}.facility__geography__county_name ;;
    view_label: "Geography"
  }

  dimension: facility__geography__locality_name {
    type: string
    label: "Locality Name"
    description: "This field denotes the specific locality/city the facility is in, I.e. Chicago or Toronto."
    sql: ${TABLE}.facility__geography__locality_name ;;
    view_label: "Geography"
  }

  dimension: facility__geography__neighbourhood_name {
    type: string
    label: "Neighbourhood Name"
    description: "This field denotes the name of the neighbourhood the facility is in, I.e. Loop or Chinatown."
    sql: ${TABLE}.facility__geography__neighbourhood_name ;;
    view_label: "Geography"
  }

  dimension: facility__geography__region_name {
    type: string
    label: "Region Name"
    description: "This field denotes the region/state/province the facility is in, I.e Illinois or Ontario."
    sql: ${TABLE}.facility__geography__region_name ;;
    view_label: "Geography"
  }

  dimension: facility__geography__geography_id {
    type: string
    label: "Geography ID"
    description: "This field denoates the unique identifier for a specific \"geograhy\", I.e. a county/region/locality/country combination."
    sql: ${TABLE}.facility__geography__geography_id ;;
    view_label: "Geography"
  }

  dimension: facility__canonical_facility__reporting_market {
    type: string
    label: "Reporting Market"
    description: "SFDC Reporting market (I.e. Region/City) of the canonical facility."
    sql: ${TABLE}.facility__canonical_facility__reporting_market ;;
    view_label: "Geography"
  }

  dimension: facility__canonical_facility__reporting_market_top_6_canada {
    type: string
    label: "Reporting Market Top 6 Canada"
    description: "Indicates if the facility is in the top 6 SFDC reporting markets in Canada."
    sql: ${TABLE}.facility__canonical_facility__reporting_market_top_6_canada ;;
    view_label: "Geography"
  }

  dimension: facility__canonical_facility__reporting_market_top_8 {
    type: string
    label: "Reporting Market Top 8"
    description: "Indicates if the facility is in SpotHero's top 8 SFDC reporting markets."
    sql: ${TABLE}.facility__canonical_facility__reporting_market_top_8 ;;
    view_label: "Geography"
  }

  dimension: rental__rental_id {
    type: string
    label: "Rental ID"
    description: "This field is the unique SpotHero Rental ID.  This ID matches the Rental ID in SpotHero Admin."
    sql: ${TABLE}.rental__rental_id ;;
    view_label: "Rental"
  }

  dimension: rental__rental_lead_time {
    type: string
    label: "Rental Lead Time"
    description: "This field denotes the minutes between the purchase time and reservation start time, in CST (negative values represent reservations purchased after the start)."
    sql: ${TABLE}.rental__rental_lead_time ;;
    view_label: "Rental"
  }

  dimension: rental__rental_length_hours {
    type: string
    label: "Rental Length Hours"
    description: "This field denotes the total length of the specific reservation attached to a rental, in hours. Note that this is not necessarily the total length of time the renter's vehicle was at the facility."
    sql: ${TABLE}.rental__rental_length_hours ;;
    view_label: "Rental"
  }

  dimension: rental__rental_length_minutes {
    type: string
    label: "Rental Length Minutes"
    description: "This field denotes the total length of the specific reservation attached to a rental, in minutes. Note that this is not necessarily the total length of time the renter's vehicle was at the facility."
    sql: ${TABLE}.rental__rental_length_minutes ;;
    view_label: "Rental"
  }

  dimension: rental__rental_payment_status {
    type: string
    label: "Rental Payment Status"
    description: "This field denotes the current status of a payment for a given rental. This field will match the status in Stripe for the same rental, and will also match what is listed in SpotHero Admin."
    sql: ${TABLE}.rental__rental_payment_status ;;
    view_label: "Rental"
  }

  dimension: rental__rental_payment_type_title {
    type: string
    label: "Rental Payment Type Title"
    description: "This field denotes the payment processing partner used for a rental (I.e. Stripe)."
    sql: ${TABLE}.rental__rental_payment_type_title ;;
    view_label: "Rental"
  }

  dimension: rental__rental_segment {
    type: string
    label: "Rental Segment"
    description: "This field denotes the rental segment of a given rental, as definied by the type of the rate purchased (Commuter, Airport, Event, Weekend PM, etc.)."
    sql: ${TABLE}.rental__rental_segment ;;
    view_label: "Rental"
  }

  dimension: rental__rental_segment_rollup {
    type: string
    label: "Rental Segment Rollup"
    description: "This field denotes a grouped rental segment of a given rental, as definied by the type of the rate purchased. Commuter, Airport, Event, and Monthly rates remain, however all other rates are grouped into Transient Rate."
    sql: ${TABLE}.rental__rental_segment_rollup ;;
    view_label: "Rental"
  }

  dimension: rental__rental_rule_type_title {
    type: string
    label: "Rental Rule Type Title"
    description: "This field denotes the specific rental type/rate attached to a rental. A rental type can be hourly, monthly, or multirate."
    sql: ${TABLE}.rental__rental_rule_type_title ;;
    view_label: "Rental"
  }

  dimension: rental__rental_source_title {
    type: string
    label: "Rental Source Title"
    description: "This field denotes the medium where the renter purchased a given rental, I.e. IOS, Android, Web."
    sql: ${TABLE}.rental__rental_source_title ;;
    view_label: "Rental"
  }

  dimension: renter__lifetime_credit_used {
    type: string
    label: "Lifetime Credit Used"
    description: "This field provides the total value of SpotHero credit used by the renter since the renter first started using the service."
    sql: ${TABLE}.renter__lifetime_credit_used ;;
    view_label: "Renter Details"
  }

  dimension: renter__lifetime_rentals {
    type: string
    label: "Lifetime Rentals"
    description: "This field provides the total number of rentals by the renter since the renter first started using the service."
    sql: ${TABLE}.renter__lifetime_rentals ;;
    view_label: "Renter Details"
  }

  dimension: renter__lifetime_value {
    type: string
    label: "Lifetime Value"
    description: "This field provides the total value of rentals made by the renter since the renter first started using the service.  This field includes ALL fees and the rental price."
    sql: ${TABLE}.renter__lifetime_value ;;
    view_label: "Renter Details"
  }

  dimension: renter__first_name {
    type: string
    label: "First Name"
    description: "This field denotes the first name of the renter."
    sql: ${TABLE}.renter__first_name ;;
    view_label: "Renter Details"
  }

  dimension: renter__last_name {
    type: string
    label: "Last Name"
    description: "This field denotes the last name of the renter."
    sql: ${TABLE}.renter__last_name ;;
    view_label: "Renter Details"
  }

  dimension: renter__first_rental_id {
    type: string
    label: "First Rental ID"
    description: "Thie field provides the unique rental Identifier for the renter's first rental."
    sql: ${TABLE}.renter__first_rental_id ;;
    view_label: "Renter Details"
  }

  dimension: renter__last_rental_id {
    type: string
    label: "Last Rental ID"
    description: "This field provides the unique rental Identifier for the renter's most recent rental."
    sql: ${TABLE}.renter__last_rental_id ;;
    view_label: "Renter Details"
  }

  dimension: renter__renter_id {
    type: string
    label: "Renter ID"
    description: "This field provides a unique identifier for the renter.  This ID pulls from Monolith."
    sql: ${TABLE}.renter__renter_id ;;
    view_label: "Renter Details"
  }

  dimension: renter__date_joined {
    type: date
    label: "Date Joined"
    description: "This field denotes the date when the renter first used a SpotHero service (includes signing up without renting)."
    sql: ${TABLE}.renter__date_joined ;;
    view_label: "Renter Details"
  }

  dimension: renter__days_since_first_rental {
    type: string
    label: "Days Since First Rental"
    description: "This field denotes the number of days elapsed since the renter's first rental."
    sql: ${TABLE}.renter__days_since_first_rental ;;
    view_label: "Renter Details"
  }

  dimension: renter__days_since_last_rental {
    type: string
    label: "Days Since Last Rental"
    description: "This field denotes the number of days elapsed since the renter's last rental."
    sql: ${TABLE}.renter__days_since_last_rental ;;
    view_label: "Renter Details"
  }

  dimension: renter__first_rental_date {
    type: date
    label: "First Rental Date"
    description: "This field denotes the date of the renter's first rental."
    sql: ${TABLE}.renter__first_rental_date ;;
    view_label: "Renter Details"
  }

  dimension: renter__last_rental_date {
    type: date
    label: "Last Rental Date"
    description: "This field denotes the date of the renter's most recent rental."
    sql: ${TABLE}.renter__last_rental_date ;;
    view_label: "Renter Details"
  }
}