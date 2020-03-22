from __future__ import division, absolute_import, print_function

from airflow.plugins_manager import AirflowPlugin

import operators
import helpers

# Defining the plugin class
class UdacityPlugin(AirflowPlugin):
    name = "udacity_plugin"
    operators = [
        operators.CopyToRedshiftOperator,
        operators.SASValueToRedshiftOperator,
        operators.DataQualityOperator
    ]
    helpers = [
        helpers.sas_source_code_tables_data,
        helpers.copy_s3_keys
    ]
