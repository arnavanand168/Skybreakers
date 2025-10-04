-- SkyHack 3.0 United Airlines Database Setup
-- This script creates tables and imports CSV data

-- Enable CSV import mode
.mode csv
.headers on

-- Create and import Airports table
CREATE TABLE Airports (
    airport_iata_code TEXT PRIMARY KEY,
    iso_country_code TEXT
);

.import "Airports Data.csv" Airports

-- Create and import Flights table (main flight data)
CREATE TABLE Flights (
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
CREATE TABLE Bags (
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
CREATE TABLE Passengers (
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
CREATE TABLE Remarks (
    record_locator TEXT,
    pnr_creation_date TEXT,
    flight_number TEXT,
    special_service_request TEXT
);

.import "PNR Remark Level Data.csv" Remarks

-- Create indexes for better performance
CREATE INDEX idx_flights_key ON Flights(company_id, flight_number, scheduled_departure_date_local);
CREATE INDEX idx_bags_key ON Bags(company_id, flight_number, scheduled_departure_date_local);
CREATE INDEX idx_passengers_key ON Passengers(company_id, flight_number, scheduled_departure_date_local);
CREATE INDEX idx_remarks_flight ON Remarks(flight_number);
CREATE INDEX idx_remarks_pnr ON Remarks(record_locator);

-- Display table counts
SELECT 'Airports' as table_name, COUNT(*) as row_count FROM Airports
UNION ALL
SELECT 'Flights', COUNT(*) FROM Flights
UNION ALL
SELECT 'Bags', COUNT(*) FROM Bags
UNION ALL
SELECT 'Passengers', COUNT(*) FROM Passengers
UNION ALL
SELECT 'Remarks', COUNT(*) FROM Remarks;
