

SELECT
    ROUND(AVG(departure_delay_minutes), 2) as avg_departure_delay_minutes,
    ROUND(AVG(arrival_delay_minutes), 2) as avg_arrival_delay_minutes
FROM MasterTable;

SELECT
    ROUND(COUNT(CASE WHEN is_delayed = 1 THEN 1 END) * 100.0 / COUNT(*), 2) as percentage_delayed_flights
FROM MasterTable;

SELECT
    COUNT(CASE WHEN ground_time_pressure > 1.5 THEN 1 END) as flights_with_low_ground_time,
    ROUND(COUNT(CASE WHEN ground_time_pressure > 1.5 THEN 1 END) * 100.0 / COUNT(*), 2) as percentage_low_ground_time
FROM MasterTable;

SELECT
    ROUND(AVG(transfer_bag_ratio), 3) as avg_transfer_bag_ratio
FROM MasterTable
WHERE total_bags > 0;

CREATE TABLE MasterTableWithFeatures AS
SELECT
    *,

    CASE
        WHEN total_seats > 0
        THEN total_passengers * 1.0 / total_seats
        ELSE 0
    END as load_factor,

    ground_time_pressure,

    transfer_bag_ratio,

    CASE
        WHEN total_passengers > 0
        THEN total_passengers_with_remarks * 1.0 / total_passengers
        ELSE 0
    END as ssr_intensity,

    is_international,

    CASE
        WHEN children_count > 0 OR lap_children_count > 0
        THEN 1
        ELSE 0
    END as has_children,

    CASE
        WHEN stroller_users > 0
        THEN 1
        ELSE 0
    END as has_strollers,

    CASE
        WHEN fleet_type LIKE '%B787%' OR fleet_type LIKE '%B777%' OR fleet_type LIKE '%B767%'
        THEN 3  -- Wide-body
        WHEN fleet_type LIKE '%B737%' OR fleet_type LIKE '%B757%' OR fleet_type LIKE '%A319%' OR fleet_type LIKE '%A320%'
        THEN 2  -- Narrow-body
        ELSE 1  -- Regional
    END as fleet_complexity,

    CASE
        WHEN CAST(strftime('%H', scheduled_departure_datetime_local) AS INTEGER) BETWEEN 5 AND 7
        THEN 3  -- Early morning
        WHEN CAST(strftime('%H', scheduled_departure_datetime_local) AS INTEGER) BETWEEN 22 AND 23
        THEN 3  -- Late night
        WHEN CAST(strftime('%H', scheduled_departure_datetime_local) AS INTEGER) BETWEEN 8 AND 9
        THEN 2  -- Morning rush
        WHEN CAST(strftime('%H', scheduled_departure_datetime_local) AS INTEGER) BETWEEN 16 AND 18
        THEN 2  -- Evening rush
        ELSE 1  -- Normal hours
    END as time_complexity

FROM MasterTable;

SELECT
    'Load Factor' as feature_name,
    ROUND(MIN(load_factor), 3) as min_value,
    ROUND(AVG(load_factor), 3) as avg_value,
    ROUND(MAX(load_factor), 3) as max_value
FROM MasterTableWithFeatures
WHERE total_seats > 0

UNION ALL

SELECT
    'Ground Time Pressure',
    ROUND(MIN(ground_time_pressure), 3),
    ROUND(AVG(ground_time_pressure), 3),
    ROUND(MAX(ground_time_pressure), 3)
FROM MasterTableWithFeatures

UNION ALL

SELECT
    'Transfer Bag Ratio',
    ROUND(MIN(transfer_bag_ratio), 3),
    ROUND(AVG(transfer_bag_ratio), 3),
    ROUND(MAX(transfer_bag_ratio), 3)
FROM MasterTableWithFeatures
WHERE total_bags > 0

UNION ALL

SELECT
    'SSR Intensity',
    ROUND(MIN(ssr_intensity), 3),
    ROUND(AVG(ssr_intensity), 3),
    ROUND(MAX(ssr_intensity), 3)
FROM MasterTableWithFeatures
WHERE total_passengers > 0;
