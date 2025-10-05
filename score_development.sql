

CREATE TABLE FeatureStats AS
SELECT
    MIN(load_factor) as min_load_factor,
    MAX(load_factor) as max_load_factor,
    MIN(ground_time_pressure) as min_ground_time_pressure,
    MAX(ground_time_pressure) as max_ground_time_pressure,
    MIN(transfer_bag_ratio) as min_transfer_bag_ratio,
    MAX(transfer_bag_ratio) as max_transfer_bag_ratio,
    MIN(ssr_intensity) as min_ssr_intensity,
    MAX(ssr_intensity) as max_ssr_intensity
FROM MasterTableWithFeatures
WHERE total_seats > 0 AND total_bags > 0 AND total_passengers > 0;

CREATE TABLE FlightDifficultyScores AS
SELECT
    *,

    CASE
        WHEN fs.max_load_factor - fs.min_load_factor > 0
        THEN (load_factor - fs.min_load_factor) / (fs.max_load_factor - fs.min_load_factor)
        ELSE 0
    END as normalized_load_factor,

    CASE
        WHEN fs.max_ground_time_pressure - fs.min_ground_time_pressure > 0
        THEN (ground_time_pressure - fs.min_ground_time_pressure) / (fs.max_ground_time_pressure - fs.min_ground_time_pressure)
        ELSE 0
    END as normalized_ground_time_pressure,

    CASE
        WHEN fs.max_transfer_bag_ratio - fs.min_transfer_bag_ratio > 0
        THEN (transfer_bag_ratio - fs.min_transfer_bag_ratio) / (fs.max_transfer_bag_ratio - fs.min_transfer_bag_ratio)
        ELSE 0
    END as normalized_transfer_bag_ratio,

    CASE
        WHEN fs.max_ssr_intensity - fs.min_ssr_intensity > 0
        THEN (ssr_intensity - fs.min_ssr_intensity) / (fs.max_ssr_intensity - fs.min_ssr_intensity)
        ELSE 0
    END as normalized_ssr_intensity,

    is_international as normalized_international,
    has_children as normalized_has_children,
    has_strollers as normalized_has_strollers,

    (fleet_complexity - 1) / 2.0 as normalized_fleet_complexity,

    (time_complexity - 1) / 2.0 as normalized_time_complexity

FROM MasterTableWithFeatures mt
CROSS JOIN FeatureStats fs;

CREATE TABLE FinalFlightScores AS
SELECT
    *,

    (normalized_ground_time_pressure * 0.25 +
     normalized_load_factor * 0.20 +
     normalized_transfer_bag_ratio * 0.20 +
     normalized_ssr_intensity * 0.15 +
     normalized_international * 0.10 +
     normalized_fleet_complexity * 0.05 +
     normalized_time_complexity * 0.05) as difficulty_score

FROM FlightDifficultyScores;

CREATE TABLE ClassifiedFlights AS
SELECT
    *,

    ROW_NUMBER() OVER (
        PARTITION BY scheduled_departure_date_local
        ORDER BY difficulty_score DESC
    ) as daily_rank,

    COUNT(*) OVER (PARTITION BY scheduled_departure_date_local) as daily_flight_count,

    CASE
        WHEN ROW_NUMBER() OVER (
            PARTITION BY scheduled_departure_date_local
            ORDER BY difficulty_score DESC
        ) <= COUNT(*) OVER (PARTITION BY scheduled_departure_date_local) * 0.20
        THEN 'Difficult'
        WHEN ROW_NUMBER() OVER (
            PARTITION BY scheduled_departure_date_local
            ORDER BY difficulty_score DESC
        ) <= COUNT(*) OVER (PARTITION BY scheduled_departure_date_local) * 0.50
        THEN 'Medium'
        ELSE 'Easy'
    END as difficulty_classification

FROM FinalFlightScores;

SELECT
    difficulty_classification,
    COUNT(*) as flight_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM ClassifiedFlights), 2) as percentage,
    ROUND(AVG(difficulty_score), 3) as avg_difficulty_score,
    ROUND(AVG(load_factor), 3) as avg_load_factor,
    ROUND(AVG(ground_time_pressure), 2) as avg_ground_time_pressure,
    ROUND(AVG(transfer_bag_ratio), 3) as avg_transfer_bag_ratio,
    ROUND(AVG(ssr_intensity), 3) as avg_ssr_intensity,
    ROUND(AVG(is_international), 3) as avg_international_ratio
FROM ClassifiedFlights
GROUP BY difficulty_classification
ORDER BY avg_difficulty_score DESC;
