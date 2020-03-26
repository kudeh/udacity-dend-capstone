from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class CopyToRedshiftOperator(BaseOperator):
    """Custom Operator for loading data into fact tables.
    
    Attributes:
        ui_color (str): color code for task in Airflow UI.
        template_fields (:obj:`tuple` of :obj: `str`): list of template parameters.
        copy_sql (str): template string for coping data from S3.   
        csv (str): csv formatting template string.
        parq (str): parquet formatting template string.
    """
    ui_color = '#426a87'
    copy_sql = """
        COPY {}
        FROM '{}'
    """
    csv = """
    ACCESS_KEY_ID '{}'
    SECRET_ACCESS_KEY '{}'
    IGNOREHEADER {}
    DELIMITER '{}'
    CSV
    """
    parq = """
    IAM_ROLE '{}'
    FORMAT AS PARQUET
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 role_arn="",
                 table="",
                 s3_bucket="",
                 s3_key="",
                 file_format="csv",
                 delimiter=",",
                 ignore_headers=1,
                 *args, **kwargs):
        """Copies csv contents to a Redshift table
        Args:
            redshift_conn_id (str): Airflow connection ID for redshift database.
            aws_credentials_id (str): Airlflow connection ID for aws key and secret.
            role_arn (str): arn role tied to redshift db.
            table (str): Name of table to quality check.
            s3_bucket (str): S3 Bucket Name.
            s3_key (str): S3 Key Name.
            file_format (str): format of file to copy to database.
            delimiter (str): csv delimiter.
            ignore_headers (int): if to ignore csv headers or not.
        """
        super(CopyToRedshiftOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.role_arn = role_arn
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.file_format = file_format
        self.delimiter = delimiter
        self.ignore_headers = ignore_headers

    def execute(self, context):
        """Executes task for staging to redshift.
        Args:
            context (:obj:`dict`): Dict with values to apply on content.
        Returns:
            None   
        """
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        self.log.info(credentials)
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.log.info('Clearing data from {}'.format(self.table))
        redshift.run('DELETE FROM {}'.format(self.table))
        
        s3_path = 's3://{}/{}'.format(self.s3_bucket, self.s3_key)
            
        self.log.info('Coping data from {} to {} on table Redshift'.format(s3_path, self.table))

        formatted_sql = CopyToRedshiftOperator.copy_sql.format(
            self.table,
            s3_path
        )

        if self.file_format=='csv':
            formatted_sql += CopyToRedshiftOperator.csv.format(
                credentials.access_key,
                credentials.secret_key,
                self.ignore_headers,
                self.delimiter
            )
        elif self.file_format=='parquet':
            formatted_sql += CopyToRedshiftOperator.parq.format(
                self.role_arn
            )
        
        self.log.info('Running Copy Command {}'.format(formatted_sql))
        redshift.run(formatted_sql)
        self.log.info('Successfully Copied data from {} to {} table on Redshift'.format(s3_path, self.table))

        