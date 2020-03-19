DROP TABLE IF EXISTS requests_raw;
DROP TABLE IF EXISTS predictions;

CREATE TABLE IF NOT EXISTS requests_raw (
	id SERIAL PRIMARY KEY,
	service_request_id INT,
	service_request_parent_id INT,
	date_requested DATE,
	case_age_days INT,
	service_name VARCHAR(100),
	case_record_type VARCHAR(100),
	date_updated TIMESTAMP,
	status VARCHAR(100),
	lat FLOAT,
	lng FLOAT,
	council_district INT,
	comm_plan_code INT,
	comm_plan_name VARCHAR(100),
	park_name VARCHAR(100),
	case_origin VARCHAR(100),
	referred VARCHAR(300),
	public_description VARCHAR,
	urgent VARCHAR(4)
);

CREATE TABLE IF NOT EXISTS predictions (
	id SERIAL PRIMARY KEY,
	service_request_id INT,
	urgent VARCHAR(4)
);
