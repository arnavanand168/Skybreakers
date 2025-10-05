

CREATE TABLE MasterTable AS
SELECT 
    f.*,

    COALESCE(bs.total_bags, 0) as total_bags,
    COALESCE(bs.transfer_bags, 0) as transfer_bags,
    COALESCE(bs.transfer_bag_ratio, 0) as transfer_bag_ratio,

    COALESCE(ps.total_passengers, 0) as total_passengers,
    COALESCE(ps.children_count, 0) as children_count,
    COALESCE(ps.lap_children_count, 0) as lap_children_count,
    COALESCE(ps.stroller_users, 0) as stroller_users,
    COALESCE(ps.basic_economy_passengers, 0) as basic_economy_passengers,

    COALESCE(sns.unique_special_requests, 0) as unique_special_requests,
    COALESCE(sns.total_special_requests, 0) as total_special_requests,
    COALESCE(sns.total_passengers_with_remarks, 0) as total_passengers_with_remarks,

    CASE 
        WHEN dep_airport.iso_country_code != 'US' OR arr_airport.iso_country_code != 'US' 
        THEN 1 
        ELSE 0 
    END as is_international,

    CASE 
        WHEN f.actual_departure_datetime_local > f.scheduled_departure_datetime_local 
        THEN 1 
        ELSE 0 
    END as is_delayed,
    
    CASE 
        WHEN f.actual_departure_datetime_local > f.scheduled_departure_datetime_local 
        THEN (julianday(f.actual_departure_datetime_local) - julianday(f.scheduled_departure_datetime_local)) * 24 * 60
        ELSE 0 
    END as departure_delay_minutes,
    
    CASE 
        WHEN f.actual_arrival_datetime_local > f.scheduled_arrival_datetime_local 
        THEN (julianday(f.actual_arrival_datetime_local) - julianday(f.scheduled_arrival_datetime_local)) * 24 * 60
        ELSE 0 
    END as arrival_delay_minutes,

    CASE 
        WHEN f.minimum_turn_minutes > 0 
        THEN f.scheduled_ground_time_minutes * 1.0 / f.minimum_turn_minutes 
        ELSE 1.0 
    END as ground_time_pressure

FROM Flights f
LEFT JOIN BagSummary bs ON f.company_id = bs.company_id 
    AND f.flight_number = bs.flight_number 
    AND f.scheduled_departure_date_local = bs.scheduled_departure_date_local
LEFT JOIN PassengerSummary ps ON f.company_id = ps.company_id 
    AND f.flight_number = ps.flight_number 
    AND f.scheduled_departure_date_local = ps.scheduled_departure_date_local
LEFT JOIN SpecialNeedsSummary sns ON f.company_id = sns.company_id 
    AND f.flight_number = sns.flight_number 
    AND f.scheduled_departure_date_local = sns.scheduled_departure_date_local
LEFT JOIN Airports dep_airport ON f.scheduled_departure_station_code = dep_airport.airport_iata_code
LEFT JOIN Airports arr_airport ON f.scheduled_arrival_station_code = arr_airport.airport_iata_code;

SELECT 
    COUNT(*) as total_flights,
    COUNT(CASE WHEN total_bags > 0 THEN 1 END) as flights_with_bags,
    COUNT(CASE WHEN total_passengers > 0 THEN 1 END) as flights_with_passengers,
    COUNT(CASE WHEN unique_special_requests > 0 THEN 1 END) as flights_with_special_requests,
    COUNT(CASE WHEN is_international = 1 THEN 1 END) as international_flights,
    COUNT(CASE WHEN is_delayed = 1 THEN 1 END) as delayed_flights,
    ROUND(AVG(departure_delay_minutes), 2) as avg_departure_delay_minutes,
    ROUND(AVG(ground_time_pressure), 2) as avg_ground_time_pressure
FROM MasterTable;
