-- SkyHack 3.0 United Airlines Flight Difficulty Scoring System
-- Complete Analysis Script by Arnav
-- 
-- This script implements a comprehensive flight difficulty scoring system
-- that analyzes operational complexity factors to help United Airlines
-- optimize their flight operations and resource allocation.

-- ==============================================
-- PHASE 1: DATA FOUNDATION AND CONSOLIDATION
-- ==============================================

-- Enable CSV import mode
.mode csv
.headers on

-- Create and import Airports table
CREATE TABLE IF NOT EXISTS Airports (
    airport_iata_code TEXT PRIMARY KEY,
    iso_country_code TEXT
);

.import "Airports Data.csv" Airports

-- Create and import Flights table (main flight data)
CREATE TABLE IF NOT EXISTS Flights (
    company_id TEXT,
    flight_number TEXT,
    scheduled_departure_date_local TEXT,
    scheduled_departure_station_code TEXT,
    scheduled_arrival_station_code TEXT,
    scheduled_departure_datetime_local TEXT,
    scheduled_arrival_datetime_local TEXT,
    actual_departure_datetime_local TEXT,
    actual_arrival_datetime_local TEXT,
    total_seats INTEGER,
    fleet_type TEXT,
    carrier TEXT,
    scheduled_ground_time_minutes INTEGER,
    actual_ground_time_minutes INTEGER,
    minimum_turn_minutes INTEGER
);

.import "Flight Level Data.csv" Flights

-- Create and import Bags table
CREATE TABLE IF NOT EXISTS Bags (
    company_id TEXT,
    flight_number TEXT,
    scheduled_departure_date_local TEXT,
    scheduled_departure_station_code TEXT,
    scheduled_arrival_station_code TEXT,
    bag_tag_unique_number TEXT,
    bag_tag_issue_date TEXT,
    bag_type TEXT
);

.import "Bag+Level+Data.csv" Bags

-- Create and import Passengers table
CREATE TABLE IF NOT EXISTS Passengers (
    company_id TEXT,
    flight_number TEXT,
    scheduled_departure_date_local TEXT,
    scheduled_departure_station_code TEXT,
    scheduled_arrival_station_code TEXT,
    record_locator TEXT,
    pnr_creation_date TEXT,
    total_pax INTEGER,
    is_child TEXT,
    basic_economy_ind INTEGER,
    is_stroller_user TEXT,
    lap_child_count INTEGER
);

.import "PNR+Flight+Level+Data.csv" Passengers

-- Create and import Remarks table
CREATE TABLE IF NOT EXISTS Remarks (
    record_locator TEXT,
    pnr_creation_date TEXT,
    flight_number TEXT,
    special_service_request TEXT
);

.import "PNR Remark Level Data.csv" Remarks

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_flights_key ON Flights(company_id, flight_number, scheduled_departure_date_local);
CREATE INDEX IF NOT EXISTS idx_bags_key ON Bags(company_id, flight_number, scheduled_departure_date_local);
CREATE INDEX IF NOT EXISTS idx_passengers_key ON Passengers(company_id, flight_number, scheduled_departure_date_local);
CREATE INDEX IF NOT EXISTS idx_remarks_flight ON Remarks(flight_number);
CREATE INDEX IF NOT EXISTS idx_remarks_pnr ON Remarks(record_locator);

-- ==============================================
-- PHASE 2: DATA AGGREGATION AND PREPROCESSING
-- ==============================================

-- 1. Summarize Bag Data: Count total_bags and transfer_bags for each unique flight
CREATE TABLE IF NOT EXISTS BagSummary AS
SELECT 
    company_id,
    flight_number,
    scheduled_departure_date_local,
    scheduled_departure_station_code,
    scheduled_arrival_station_code,
    COUNT(*) as total_bags,
    SUM(CASE WHEN bag_type = 'Transfer' THEN 1 ELSE 0 END) as transfer_bags,
    SUM(CASE WHEN bag_type = 'Transfer' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) as transfer_bag_ratio
FROM Bags
GROUP BY company_id, flight_number, scheduled_departure_date_local, 
         scheduled_departure_station_code, scheduled_arrival_station_code;

-- 2. Summarize Passenger Data: Sum total_passengers and count children/lap children for each unique flight
CREATE TABLE IF NOT EXISTS PassengerSummary AS
SELECT 
    company_id,
    flight_number,
    scheduled_departure_date_local,
    scheduled_departure_station_code,
    scheduled_arrival_station_code,
    SUM(total_pax) as total_passengers,
    SUM(CASE WHEN is_child = 'Y' THEN total_pax ELSE 0 END) as children_count,
    SUM(lap_child_count) as lap_children_count,
    SUM(CASE WHEN is_stroller_user = 'Y' THEN 1 ELSE 0 END) as stroller_users,
    SUM(CASE WHEN basic_economy_ind = 1 THEN total_pax ELSE 0 END) as basic_economy_passengers
FROM Passengers
GROUP BY company_id, flight_number, scheduled_departure_date_local,
         scheduled_departure_station_code, scheduled_arrival_station_code;

-- 3. Summarize Special Needs Data: Join Remarks with Passengers, then count unique special_service_requests
CREATE TABLE IF NOT EXISTS SpecialNeedsSummary AS
SELECT 
    p.company_id,
    p.flight_number,
    p.scheduled_departure_date_local,
    p.scheduled_departure_station_code,
    p.scheduled_arrival_station_code,
    COUNT(DISTINCT r.special_service_request) as unique_special_requests,
    COUNT(r.special_service_request) as total_special_requests,
    SUM(p.total_pax) as total_passengers_with_remarks
FROM Passengers p
INNER JOIN Remarks r ON p.record_locator = r.record_locator
GROUP BY p.company_id, p.flight_number, p.scheduled_departure_date_local,
         p.scheduled_departure_station_code, p.scheduled_arrival_station_code;

-- ==============================================
-- PHASE 3: MASTER TABLE CONSTRUCTION
-- ==============================================

-- Build Master Table by joining all summarized data
CREATE TABLE IF NOT EXISTS MasterTable AS
SELECT 
    f.*,
    -- Bag data (LEFT JOIN to preserve flights without bags)
    COALESCE(bs.total_bags, 0) as total_bags,
    COALESCE(bs.transfer_bags, 0) as transfer_bags,
    COALESCE(bs.transfer_bag_ratio, 0) as transfer_bag_ratio,
    
    -- Passenger data (LEFT JOIN to preserve flights without passengers)
    COALESCE(ps.total_passengers, 0) as total_passengers,
    COALESCE(ps.children_count, 0) as children_count,
    COALESCE(ps.lap_children_count, 0) as lap_children_count,
    COALESCE(ps.stroller_users, 0) as stroller_users,
    COALESCE(ps.basic_economy_passengers, 0) as basic_economy_passengers,
    
    -- Special needs data (LEFT JOIN to preserve flights without special requests)
    COALESCE(sns.unique_special_requests, 0) as unique_special_requests,
    COALESCE(sns.total_special_requests, 0) as total_special_requests,
    COALESCE(sns.total_passengers_with_remarks, 0) as total_passengers_with_remarks,
    
    -- Airport data for international flights
    CASE 
        WHEN dep_airport.iso_country_code != 'US' OR arr_airport.iso_country_code != 'US' 
        THEN 1 
        ELSE 0 
    END as is_international,
    
    -- Calculate delay metrics
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
    
    -- Ground time pressure
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

-- ==============================================
-- PHASE 4: FEATURE ENGINEERING
-- ==============================================

-- Feature Engineering: Create difficulty driver features
CREATE TABLE IF NOT EXISTS MasterTableWithFeatures AS
SELECT 
    *,
    
    -- Load factor: percentage of seats that are filled
    CASE 
        WHEN total_seats > 0 
        THEN total_passengers * 1.0 / total_seats 
        ELSE 0 
    END as load_factor,
    
    -- Ground time pressure: ratio comparing scheduled ground time to minimum required time
    ground_time_pressure,
    
    -- Transfer bag ratio: proportion of all bags that are transfers
    transfer_bag_ratio,
    
    -- SSR intensity: proportion of passengers who have special service requests
    CASE 
        WHEN total_passengers > 0 
        THEN total_passengers_with_remarks * 1.0 / total_passengers 
        ELSE 0 
    END as ssr_intensity,
    
    -- International flag
    is_international,
    
    -- Additional features for difficulty scoring
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
    
    -- Fleet complexity (larger aircraft = more complex)
    CASE 
        WHEN fleet_type LIKE '%B787%' OR fleet_type LIKE '%B777%' OR fleet_type LIKE '%B767%' 
        THEN 3  -- Wide-body
        WHEN fleet_type LIKE '%B737%' OR fleet_type LIKE '%B757%' OR fleet_type LIKE '%A319%' OR fleet_type LIKE '%A320%' 
        THEN 2  -- Narrow-body
        ELSE 1  -- Regional
    END as fleet_complexity,
    
    -- Time of day complexity (early morning and late night are more complex)
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

-- ==============================================
-- PHASE 5: SCORE DEVELOPMENT AND NORMALIZATION
-- ==============================================

-- Get the min/max values for normalization
CREATE TABLE IF NOT EXISTS FeatureStats AS
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

-- Create final table with normalized features and difficulty score
CREATE TABLE IF NOT EXISTS FlightDifficultyScores AS
SELECT 
    *,
    
    -- Normalize features using Min-Max normalization (0 to 1 scale)
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
    
    -- Normalize binary features (already 0-1, but ensure consistency)
    is_international as normalized_international,
    has_children as normalized_has_children,
    has_strollers as normalized_has_strollers,
    
    -- Normalize fleet complexity (1-3 scale to 0-1)
    (fleet_complexity - 1) / 2.0 as normalized_fleet_complexity,
    
    -- Normalize time complexity (1-3 scale to 0-1)
    (time_complexity - 1) / 2.0 as normalized_time_complexity

FROM MasterTableWithFeatures mt
CROSS JOIN FeatureStats fs;

-- Calculate Flight Difficulty Score with business-defined weights
CREATE TABLE IF NOT EXISTS FinalFlightScores AS
SELECT 
    *,
    
    -- Define weights (must sum to 1.0)
    -- Ground time pressure: 25% (most critical for operations)
    -- Load factor: 20% (capacity utilization)
    -- Transfer bag ratio: 20% (baggage complexity)
    -- SSR intensity: 15% (special service complexity)
    -- International: 10% (regulatory complexity)
    -- Fleet complexity: 5% (aircraft complexity)
    -- Time complexity: 5% (operational timing)
    
    (normalized_ground_time_pressure * 0.25 +
     normalized_load_factor * 0.20 +
     normalized_transfer_bag_ratio * 0.20 +
     normalized_ssr_intensity * 0.15 +
     normalized_international * 0.10 +
     normalized_fleet_complexity * 0.05 +
     normalized_time_complexity * 0.05) as difficulty_score

FROM FlightDifficultyScores;

-- ==============================================
-- PHASE 6: CLASSIFICATION AND RANKING
-- ==============================================

-- Add daily rankings and classifications
CREATE TABLE IF NOT EXISTS ClassifiedFlights AS
SELECT 
    *,
    
    -- Rank flights by difficulty score within each day
    ROW_NUMBER() OVER (
        PARTITION BY scheduled_departure_date_local 
        ORDER BY difficulty_score DESC
    ) as daily_rank,
    
    -- Count total flights per day for percentage calculation
    COUNT(*) OVER (PARTITION BY scheduled_departure_date_local) as daily_flight_count,
    
    -- Classify flights based on daily ranking (top 20% = Difficult, next 30% = Medium, bottom 50% = Easy)
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

-- ==============================================
-- PHASE 7: BUSINESS INSIGHTS AND ANALYSIS
-- ==============================================

-- Display classification summary
SELECT 
    '=== CLASSIFICATION SUMMARY ===' as analysis_type,
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

-- Top 10 destinations that most frequently appear in "Difficult" category
SELECT 
    '=== TOP DIFFICULT DESTINATIONS ===' as analysis_type,
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

-- Fleet type analysis for difficult flights
SELECT 
    '=== FLEET TYPE ANALYSIS ===' as analysis_type,
    fleet_type,
    COUNT(*) as total_flights,
    COUNT(CASE WHEN difficulty_classification = 'Difficult' THEN 1 END) as difficult_flights,
    ROUND(COUNT(CASE WHEN difficulty_classification = 'Difficult' THEN 1 END) * 100.0 / COUNT(*), 2) as difficult_percentage,
    ROUND(AVG(difficulty_score), 3) as avg_difficulty_score
FROM ClassifiedFlights
GROUP BY fleet_type
ORDER BY difficult_percentage DESC;

-- Time of day analysis for difficult flights
SELECT 
    '=== TIME OF DAY ANALYSIS ===' as analysis_type,
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

-- ==============================================
-- PHASE 8: EXPORT RESULTS
-- ==============================================

-- Export final results to CSV
.headers on
.mode csv

.output test_arnav.csv
SELECT 
    company_id,
    flight_number,
    scheduled_departure_date_local,
    scheduled_departure_station_code,
    scheduled_arrival_station_code,
    scheduled_departure_datetime_local,
    scheduled_arrival_datetime_local,
    actual_departure_datetime_local,
    actual_arrival_datetime_local,
    total_seats,
    fleet_type,
    carrier,
    scheduled_ground_time_minutes,
    actual_ground_time_minutes,
    minimum_turn_minutes,
    total_bags,
    transfer_bags,
    transfer_bag_ratio,
    total_passengers,
    children_count,
    lap_children_count,
    stroller_users,
    basic_economy_passengers,
    unique_special_requests,
    total_special_requests,
    total_passengers_with_remarks,
    is_international,
    is_delayed,
    departure_delay_minutes,
    arrival_delay_minutes,
    ground_time_pressure,
    load_factor,
    ssr_intensity,
    has_children,
    has_strollers,
    fleet_complexity,
    time_complexity,
    normalized_load_factor,
    normalized_ground_time_pressure,
    normalized_transfer_bag_ratio,
    normalized_ssr_intensity,
    normalized_international,
    normalized_has_children,
    normalized_has_strollers,
    normalized_fleet_complexity,
    normalized_time_complexity,
    difficulty_score,
    daily_rank,
    daily_flight_count,
    difficulty_classification
FROM ClassifiedFlights
ORDER BY scheduled_departure_date_local, difficulty_score DESC;

-- Reset output
.output stdout
.mode column
.headers on

-- Final summary
SELECT '=== ANALYSIS COMPLETE ===' as status;
SELECT 'Total flights analyzed: ' || COUNT(*) as summary FROM ClassifiedFlights;
SELECT 'Difficult flights: ' || COUNT(CASE WHEN difficulty_classification = 'Difficult' THEN 1 END) as summary FROM ClassifiedFlights;
SELECT 'Medium flights: ' || COUNT(CASE WHEN difficulty_classification = 'Medium' THEN 1 END) as summary FROM ClassifiedFlights;
SELECT 'Easy flights: ' || COUNT(CASE WHEN difficulty_classification = 'Easy' THEN 1 END) as summary FROM ClassifiedFlights;
