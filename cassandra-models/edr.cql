CREATE KEYSPACE IF NOT EXISTS cdr WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '3'}  AND durable_writes = true;

CREATE TYPE IF NOT EXISTS cdr.product(
  id  TEXT,
  name TEXT
);

CREATE TYPE IF NOT EXISTS cdr.location_information(
  destination TEXT,
  location_number TEXT,
  location_area_identification TEXT,
  cell_global_idenfitifaction TEXT
);

CREATE TYPE IF NOT EXISTS cdr.service_unit(
  amount DECIMAL,
  currency TEXT,
  unit_of_measure TEXT
);

CREATE TYPE IF NOT EXISTS cdr.charged_amount(
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
  a_party_location frozen<location_information>,
  b_party_number TEXT,
  b_party_location frozen<location_information>
);

CREATE TYPE IF NOT EXISTS cdr.data_event_details(
  access_point_name TEXT,
  is_roaming BOOLEAN,
  a_party_number TEXT,
  a_party_location frozen<location_information>,
);

CREATE TYPE IF NOT EXISTS cdr.event_charges(
  event_units frozen<service_unit>,
  product_info frozen<product>,
  charged_amounts list<frozen<charged_amount>>
);

CREATE TABLE IF NOT EXISTS cdr.edr (
    id TEXT PRIMARY KEY,
    service TEXT,
    created_at TIMESTAMP,
    started_at TIMESTAMP,
    used_service_units frozen<service_unit>,
    call_event frozen<call_event_details>,
    data_event frozen<data_event_details>
);
