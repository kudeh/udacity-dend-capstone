# Udacity Data Engineering Nanodegree Capstone Project
##### Table of Contents  
- [Introduction](#introduction)
- [Set Up](#setup)
- [Usage](#usage)

## Introduction
For my capstone project I developed a data pipeline that creates an analytics database for querying information about immigration into the U.S on a monthly basis. The analytics tables are hosted in a Redshift Database and the pipeline implementation was done using Apache Airflow.

View [Notebook](https://github.com/kudeh/udacity-dend-capstone/blob/master/Capstone%20EDA.ipynb) for more details.

### Datasets
The following datasets were used to create the analytics database:
* I94 Immigration Data: This data comes from the US National Tourism and Trade Office found [here](https://travel.trade.gov/research/reports/i94/historical/2016.html). Each report contains international visitor arrival statistics by world regions and select countries (including top 20), type of visa, mode of transportation, age groups, states visited (first intended address only), and the top ports of entry (for select countries).
* World Temperature Data: This dataset came from Kaggle found [here](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data).
* U.S. City Demographic Data: This dataset contains information about the demographics of all US cities and census-designated places with a population greater or equal to 65,000. Dataset comes from OpenSoft found [here](https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/).
* Airport Code Table: This is a simple table of airport codes and corresponding cities. The airport codes may refer to either IATA airport code, a three-letter code which is used in passenger reservation, ticketing and baggage-handling systems, or the ICAO airport code which is a four letter code used by ATC systems and for airports that do not have an IATA airport code (from wikipedia). It comes from [here](https://datahub.io/core/airport-codes#data).

### Data Model
The data model consists of tables `immigration`, `us_cities_demographics`, `airport_codes`, `world_temperature`, `i94cit_res`, `i94port`, `i94mode`, `i94addr`, `i94visa`
<img src="README_IMGS/ERD.jpg"/>

### Data Pipeline
<img src="README_IMGS/dag.png"/>

### Example Queries

## Setup
1. Python3 & Java 8 Required
2. Create virtual environment and install dependencies
    ```bash
    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt
    (venv) $ ipython kernel install --user --name=projectname
    ```
3. set java version to java8 if not default
    ```bash
    (venv) $ export JAVA_HOME=`/usr/libexec/java_home -v 1.8`
    ```
4. create aws config
   * create file `dwh.cfg`
   * add the following contents (fill the fields)
    ```bash
    [CLUSTER]
    HOST=
    DB_NAME=
    DB_USER=
    DB_PASSWORD=
    DB_PORT=
    ARN=

    [S3]
    BUCKET=
   ```
5. Initialize Airflow & Run Webserver
    ```bash
    (venv) $ export AIRFLOW_HOME=$(pwd)
    (venv) $ airflow initdb
    (venv) $ airflow webserver -p 8080
    ```
6. Run Scheduler (Open New Terminal Tab)
    ```bash
    (venv) $ export AIRFLOW_HOME=$(pwd)
    (venv) $ airflow scheduler
    ```

## Usage
1. Create Tables:
    ```bash
    (venv) $ python create_tables.py
    ```
2. Access Airflow UI at `localhost:8080`
3. Create Airflow Connections:
    * AWS connection:
    <img src="README_IMGS/aws_credentials.png"/>
    * Redshift connection
    <img src="README_IMGS/redshift.png"/>
4. Run `etl_dag` in Airflow UI