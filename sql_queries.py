table_list = ['immigration', 'us_cities_demographics', 'airport_codes', 'world_temperature',
              'i94cit_res', 'i94port', 'i94mode', 'i94addr', 'i94visa']

drop_table_template = "DROP TABLE IF EXISTS {schema}.{table}"

create_table_immigration = """
CREATE TABLE IF NOT EXISTS public.immigration (
    cicid INT,
    i94yr INT,
    i94mon INT,
    i94cit INTEGER,
    i94res INT,
    i94port CHAR(3),
    arrdate DATE,
    i94mode INT,
    i94addr INT,
    depdate DATE,
    i94bir INT,
    i94visa INT,
    count INT,
    dtadfile DATE,
    visapost CHAR(3),
    occup CHAR(3),
    entdepa CHAR(1),
    entdepd CHAR(1),
    entdepu CHAR(1),
    matflag CHAR(1),
    biryear INT,
    dtaddto DATE,
    gender CHAR(1),
    insnum INT,
    airline CHAR(2),
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
    state_code CHAR(2),
    race VARCHAR,
    count INT
);
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
    coordinates VARCHAR,
    lat FLOAT,
    long FLOAT
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
    code INT,
    country VARCHAR
);
"""

create_i94port = """
CREATE TABLE IF NOT EXISTS public.i94port (
    code CHAR(3),
    port VARCHAR
);
"""

create_i94mode = """
CREATE TABLE IF NOT EXISTS public.i94mode (
    code INT,
    mode VARCHAR
);
"""

create_i94addr = """
CREATE TABLE IF NOT EXISTS public.i94addr (
    code CHAR(2),
    addr VARCHAR
);
"""

create_i94visa = """
CREATE TABLE IF NOT EXISTS public.i94visa (
    code INT,
    type VARCHAR
);
"""

drop_table_queries = [drop_table_template.format('public', t) for t in table_list]
create_table_queries = [create_table_immigration, create_us_cities_demographics,
create_airport_codes, create_world_temperature, create_i94cit_res, create_i94port,
create_i94mode, create_i94addr, create_i94visa]