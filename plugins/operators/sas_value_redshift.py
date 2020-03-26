import pandas as pd
import boto3

from sqlalchemy import create_engine, text

from airflow.hooks.base_hook import BaseHook
from airflow.hooks.S3_hook import S3Hook
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class SASValueToRedshiftOperator(BaseOperator):
    """Custom Operator for extracting data from SAS source code.
    Attributes:
        ui_color (str): color code for task in Airflow UI.
    """
    ui_color = '#358150'

    @apply_defaults
    def __init__(self,
                 aws_credentials_id="",
                 redshift_conn_id="",
                 table="",
                 s3_bucket="",
                 s3_key="",
                 sas_value="",
                 columns="",
                 *args, **kwargs):
        """Extracts label mappings from SAS source code and store as Redshift table
        Args:
            aws_credentials_id (str): Airflow connection ID for AWS key and secret.
            redshift_conn_id (str): Airflow connection ID for redshift database.
            table (str): Name of table to load data to.
            s3_bucket (str): S3 Bucket Name Where SAS source code is store.
            s3_key (str): S3 Key Name for SAS source code.
            sas_value (str): value to search for in sas file for extraction of data.
            columns (list): resulting data column names.
        Returns:
            None
        """
        super(SASValueToRedshiftOperator, self).__init__(*args, **kwargs)
        self.aws_credentials_id = aws_credentials_id
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.sas_value = sas_value
        self.columns = columns
    
    def execute(self, context):
        """Executes task for staging to redshift.
        Args:
            context (:obj:`dict`): Dict with values to apply on content.
        Returns:
            None   
        """
        s3 = S3Hook(self.aws_credentials_id)

        redshift_conn = BaseHook.get_connection(self.redshift_conn_id)
        self.log.info('Connecting to {}...'.format(redshift_conn.host))
        conn = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
                             redshift_conn.login,
                             redshift_conn.password,
                             redshift_conn.host,
                             redshift_conn.port,
                             redshift_conn.schema
                            ))
        self.log.info('Connected!')

        self.log.info('Reading From S3: s3://{}/{}'.format(self.s3_bucket, self.s3_key))
        file_string = s3.read_key(self.s3_key, self.s3_bucket)
        self.log.info('File has {} characters'.format(len(file_string)))

        file_string = file_string[file_string.index(self.sas_value):]
        file_string = file_string[:file_string.index(';')]
        
        line_list = file_string.split('\n')[1:]
        codes = []
        values = []
        
        self.log.info('Parsing SAS file: {}/{}'.format(self.s3_bucket, self.s3_key))
        for line in line_list:
            
            if '=' in line:
                code, val = line.split('=')
                code = code.strip()
                val = val.strip()
                
                if code[0] == "'":
                    code = code[1:-1]
                    
                if val[0] == "'":
                    val = val[1:-1]
                    
                codes.append(code)
                values.append(val)

        self.log.info('Converting parsed data to dataframe...')
        df = pd.DataFrame(list(zip(codes,values)), columns=self.columns)

        self.log.info(f'Truncating table: {self.table}')
        truncate_query = text(f'TRUNCATE TABLE {self.table}')
        conn.execution_options(autocommit=True).execute(truncate_query)

        self.log.info('Writing result to table {}'.format(self.table))
        df.to_sql(self.table, conn, index=False, if_exists='append')
        conn.dispose()




