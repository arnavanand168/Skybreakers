CREATE TABLE BagSummary AS
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

CREATE TABLE PassengerSummary AS
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

CREATE TABLE SpecialNeedsSummary AS
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

SELECT 'BagSummary' as table_name, COUNT(*) as row_count FROM BagSummary
UNION ALL
SELECT 'PassengerSummary', COUNT(*) FROM PassengerSummary
UNION ALL
SELECT 'SpecialNeedsSummary', COUNT(*) FROM SpecialNeedsSummary;
