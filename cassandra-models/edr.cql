CREATE KEYSPACE IF NOT EXISTS cdr WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '3'}  AND durable_writes = true;

CREATE TYPE IF NOT EXISTS cdr.products(
  id  TEXT,
  name TEXT
);

CREATE TYPE IF NOT EXISTS cdr.location_information(
  destination TEXT,
  location_number TEXT,
  location_area_identification TEXT,
  cell_global_idenfitifaction TEXT
);

CREATE TYPE IF NOT EXISTS cdr.service_units(
  amount DECIMAL,
  currency TEXT,
  unit_of_measure TEXT
);

CREATE TYPE IF NOT EXISTS cdr.charged_amounts(
  id TEXT,
  name TEXT,
  charged_type TEXT,
  event_type TEXT,
  resource_type TEXT,
  amount DECIMAL,
  end_balance DECIMAL,
  expiry_date TIMESTAMP
);

CREATE TYPE IF NOT EXISTS cdr.call_event_details(
  traffic_case TEXT,
  event_type TEXT,
  is_roaming BOOLEAN,
  a_party_number TEXT,
  a_party_location frozen<cdr.location_information>,
  b_party_number TEXT,
  b_party_location frozen<cdr.location_information>
);

CREATE TYPE IF NOT EXISTS cdr.data_event_details(
  access_point_name TEXT,
  is_roaming BOOLEAN,
  a_party_number TEXT,
  a_party_location frozen<cdr.location_information>,
);

CREATE TYPE IF NOT EXISTS cdr.event_charges(
  charged_units frozen<cdr.service_units>,
  products frozen<cdr.products>,
  charged_amounts list<frozen<cdr.charged_amounts>>
);

CREATE TABLE IF NOT EXISTS cdr.edr_by_id (
    id TEXT PRIMARY KEY,
    service TEXT,
    created_at TIMESTAMP,
    started_at TIMESTAMP,
    service_units frozen<cdr.service_units>,
    event_charges frozen<cdr.event_charges>,
    call_event frozen<call_event_details>,
    data_event frozen<data_event_details>
);
CREATE INDEX IF NOT EXISTS ON cdr.edr_by_id (started_at);

CREATE TABLE IF NOT EXISTS cdr.edr_by_date (
    id TEXT,
    service TEXT,
    created_at TIMESTAMP,
    started_at TIMESTAMP,
    service_units frozen<cdr.service_units>,
    event_charges frozen<cdr.event_charges>,
    call_event frozen<call_event_details>,
    data_event frozen<data_event_details>,
    PRIMARY KEY (started_at, id)
);
CREATE INDEX IF NOT EXISTS ON cdr.edr_by_date (created_at);

CREATE TABLE IF NOT EXISTS cdr.edr_by_service (
    id TEXT,
    service TEXT,
    created_at TIMESTAMP,
    started_at TIMESTAMP,
    service_units frozen<cdr.service_units>,
    event_charges frozen<cdr.event_charges>,
    call_event frozen<call_event_details>,
    data_event frozen<data_event_details>,
    PRIMARY KEY (service, started_at)
);
CREATE INDEX IF NOT EXISTS ON cdr.edr_by_service (created_at);

CREATE TABLE IF NOT EXISTS cdr.edr_by_destination (
    id TEXT,
    destination TEXT,
    service TEXT,
    created_at TIMESTAMP,
    started_at TIMESTAMP,
    service_units frozen<cdr.service_units>,
    event_charges frozen<cdr.event_charges>,
    call_event frozen<call_event_details>,
    data_event frozen<data_event_details>,
    PRIMARY KEY (destination, id)
);
CREATE INDEX IF NOT EXISTS ON cdr.edr_by_destination (started_at);

CREATE TABLE IF NOT EXISTS cdr.edr_by_date2 (
    id TEXT,
    service TEXT,
    created_at TIMESTAMP,
    started_at TIMESTAMP,
    service_units frozen<cdr.service_units>,
    event_charges frozen<cdr.event_charges>,
    call_event frozen<call_event_details>,
    data_event frozen<data_event_details>,
    PRIMARY KEY (created_at, id)
);
CREATE INDEX IF NOT EXISTS ON cdr.edr_by_date2 (started_at);

CREATE TABLE IF NOT EXISTS cdr.edr_by_id2 (
    id TEXT,
    service TEXT,
    created_at TIMESTAMP,
    started_at TIMESTAMP,
    service_units frozen<cdr.service_units>,
    event_charges frozen<cdr.event_charges>,
    call_event frozen<call_event_details>,
    data_event frozen<data_event_details>,
    PRIMARY KEY (id, created_at)
);
CREATE INDEX IF NOT EXISTS ON cdr.edr_by_id2 (started_at);
