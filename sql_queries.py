table_list = ['immigration', 'us_cities_demographics', 'airport_codes', 'world_temperature',
              'i94cit_res', 'i94port', 'i94mode', 'i94addr', 'i94visa']

drop_table_template = "DROP TABLE IF EXISTS {}.{}"

create_table_immigration = """
CREATE TABLE IF NOT EXISTS public.immigration (
    cicid FLOAT PRIMARY KEY,
    i94yr FLOAT SORTKEY,
    i94mon FLOAT DISTKEY,
    i94cit FLOAT REFERENCES i94cit_res(code),
    i94res FLOAT REFERENCES i94cit_res(code),
    i94port CHAR(3) REFERENCES i94port(code),
    arrdate FLOAT,
    i94mode FLOAT REFERENCES i94mode(code),
    i94addr VARCHAR REFERENCES i94addr(code),
    depdate FLOAT,
    i94bir FLOAT,
    i94visa FLOAT REFERENCES i94visa(code),
    count FLOAT,
    dtadfile VARCHAR,
    visapost CHAR(3),
    occup CHAR(3),
    entdepa CHAR(1),
    entdepd CHAR(1),
    entdepu CHAR(1),
    matflag CHAR(1),
    biryear FLOAT,
    dtaddto VARCHAR,
    gender CHAR(1),
    insnum VARCHAR,
    airline VARCHAR,
    admnum FLOAT,
    fltno VARCHAR,
    visatype VARCHAR
);
"""

create_us_cities_demographics = """
CREATE TABLE IF NOT EXISTS public.us_cities_demographics (
    city VARCHAR,
    state VARCHAR,
    median_age FLOAT,
    male_population INT,
    female_population INT,
    total_population INT,
    number_of_veterans INT,
    foreign_born INT,
    average_household_size FLOAT,
    state_code CHAR(2) REFERENCES i94addr(code),
    race VARCHAR,
    count INT
)
DISTSTYLE ALL
"""

create_airport_codes = """
CREATE TABLE IF NOT EXISTS public.airport_codes (
    ident VARCHAR,
    type VARCHAR,
    name VARCHAR,
    elevation_ft FLOAT,
    continent VARCHAR,
    iso_country VARCHAR,
    iso_region VARCHAR,
    municipality VARCHAR,
    gps_code VARCHAR,
    iata_code VARCHAR,
    local_code VARCHAR,
    coordinates VARCHAR
);
"""

create_world_temperature = """
CREATE TABLE IF NOT EXISTS public.world_temperature (
    dt DATE,
    AverageTemperature FLOAT,
    AverageTemperatureUncertainty FLOAT,
    City VARCHAR,
    Country VARCHAR,
    Latitude VARCHAR,
    Longitude VARCHAR
);
"""

create_i94cit_res = """
CREATE TABLE IF NOT EXISTS public.i94cit_res (
    code FLOAT PRIMARY KEY,
    country VARCHAR
)
DISTSTYLE ALL
"""

create_i94port = """
CREATE TABLE IF NOT EXISTS public.i94port (
    code CHAR(3) PRIMARY KEY,
    port VARCHAR
)
DISTSTYLE ALL
"""

create_i94mode = """
CREATE TABLE IF NOT EXISTS public.i94mode (
    code FLOAT PRIMARY KEY,
    mode VARCHAR
)
DISTSTYLE ALL
"""

create_i94addr = """
CREATE TABLE IF NOT EXISTS public.i94addr (
    code CHAR(2) PRIMARY KEY,
    addr VARCHAR
)
DISTSTYLE ALL
"""

create_i94visa = """
CREATE TABLE IF NOT EXISTS public.i94visa (
    code FLOAT PRIMARY KEY,
    type VARCHAR
)
DISTSTYLE ALL
"""

drop_table_queries = [drop_table_template.format('public', t) for t in table_list]
create_table_queries = [create_i94cit_res, create_i94port,
create_i94mode, create_i94addr, create_i94visa, create_table_immigration, create_us_cities_demographics,
create_airport_codes, create_world_temperature]