

SELECT 
    scheduled_arrival_station_code as destination,
    COUNT(*) as difficult_flight_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM ClassifiedFlights WHERE difficulty_classification = 'Difficult'), 2) as percentage_of_difficult_flights,
    ROUND(AVG(difficulty_score), 3) as avg_difficulty_score,
    ROUND(AVG(load_factor), 3) as avg_load_factor,
    ROUND(AVG(ground_time_pressure), 2) as avg_ground_time_pressure,
    ROUND(AVG(transfer_bag_ratio), 3) as avg_transfer_bag_ratio,
    ROUND(AVG(ssr_intensity), 3) as avg_ssr_intensity,
    ROUND(AVG(is_international), 3) as avg_international_ratio
FROM ClassifiedFlights
WHERE difficulty_classification = 'Difficult'
GROUP BY scheduled_arrival_station_code
ORDER BY difficult_flight_count DESC
LIMIT 10;

SELECT 
    'Top Difficult Destinations Analysis' as analysis_type,
    scheduled_arrival_station_code as destination,
    COUNT(*) as total_flights,
    COUNT(CASE WHEN difficulty_classification = 'Difficult' THEN 1 END) as difficult_flights,
    ROUND(AVG(CASE WHEN difficulty_classification = 'Difficult' THEN ground_time_pressure END), 2) as difficult_avg_ground_pressure,
    ROUND(AVG(CASE WHEN difficulty_classification = 'Difficult' THEN load_factor END), 3) as difficult_avg_load_factor,
    ROUND(AVG(CASE WHEN difficulty_classification = 'Difficult' THEN transfer_bag_ratio END), 3) as difficult_avg_transfer_ratio,
    ROUND(AVG(CASE WHEN difficulty_classification = 'Difficult' THEN ssr_intensity END), 3) as difficult_avg_ssr_intensity,
    ROUND(AVG(CASE WHEN difficulty_classification = 'Difficult' THEN is_international END), 3) as difficult_avg_international
FROM ClassifiedFlights
WHERE scheduled_arrival_station_code IN (
    SELECT scheduled_arrival_station_code 
    FROM ClassifiedFlights 
    WHERE difficulty_classification = 'Difficult'
    GROUP BY scheduled_arrival_station_code
    ORDER BY COUNT(*) DESC
    LIMIT 5
)
GROUP BY scheduled_arrival_station_code
ORDER BY difficult_flights DESC;

SELECT 
    fleet_type,
    COUNT(*) as total_flights,
    COUNT(CASE WHEN difficulty_classification = 'Difficult' THEN 1 END) as difficult_flights,
    ROUND(COUNT(CASE WHEN difficulty_classification = 'Difficult' THEN 1 END) * 100.0 / COUNT(*), 2) as difficult_percentage,
    ROUND(AVG(difficulty_score), 3) as avg_difficulty_score
FROM ClassifiedFlights
GROUP BY fleet_type
ORDER BY difficult_percentage DESC;

SELECT 
    CASE 
        WHEN CAST(strftime('%H', scheduled_departure_datetime_local) AS INTEGER) BETWEEN 5 AND 7 THEN 'Early Morning (5-7)'
        WHEN CAST(strftime('%H', scheduled_departure_datetime_local) AS INTEGER) BETWEEN 8 AND 11 THEN 'Morning (8-11)'
        WHEN CAST(strftime('%H', scheduled_departure_datetime_local) AS INTEGER) BETWEEN 12 AND 15 THEN 'Afternoon (12-15)'
        WHEN CAST(strftime('%H', scheduled_departure_datetime_local) AS INTEGER) BETWEEN 16 AND 19 THEN 'Evening (16-19)'
        WHEN CAST(strftime('%H', scheduled_departure_datetime_local) AS INTEGER) BETWEEN 20 AND 23 THEN 'Night (20-23)'
        ELSE 'Other'
    END as time_period,
    COUNT(*) as total_flights,
    COUNT(CASE WHEN difficulty_classification = 'Difficult' THEN 1 END) as difficult_flights,
    ROUND(COUNT(CASE WHEN difficulty_classification = 'Difficult' THEN 1 END) * 100.0 / COUNT(*), 2) as difficult_percentage,
    ROUND(AVG(difficulty_score), 3) as avg_difficulty_score
FROM ClassifiedFlights
GROUP BY time_period
ORDER BY difficult_percentage DESC;

SELECT 
    carrier,
    COUNT(*) as total_flights,
    COUNT(CASE WHEN difficulty_classification = 'Difficult' THEN 1 END) as difficult_flights,
    ROUND(COUNT(CASE WHEN difficulty_classification = 'Difficult' THEN 1 END) * 100.0 / COUNT(*), 2) as difficult_percentage,
    ROUND(AVG(difficulty_score), 3) as avg_difficulty_score
FROM ClassifiedFlights
GROUP BY carrier
ORDER BY difficult_percentage DESC;
