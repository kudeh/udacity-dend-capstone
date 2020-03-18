from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    """Custom Operator for loading data into fact tables.
    
    Attributes:
        ui_color (str): color code for task in Airflow UI.
        template_fields (:obj:`tuple` of :obj: `str`): list of template parameters.
        copy_sql (str): template string for coping data from S3.
        
    """
    ui_color = '#358140'
    template_fields = ("partition_template",)
    copy_sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        FORMAT AS JSON '{}'
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 table="",
                 s3_bucket="",
                 s3_key="",
                 json_paths="",
                 use_partitioned=False,
                 partition_template="",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.json_paths = json_paths
        self.use_partitioned = use_partitioned
        self.partition_template = partition_template

    def execute(self, context):
        """Executes task for staging to redshift.
        Args:
            context (:obj:`dict`): Dict with values to apply on content.
            
        """
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.log.info('Clearing data from {}'.format(self.table))
        redshift.run('DELETE FROM {}'.format(self.table))
        
       
        s3_path = 's3://{}/{}'.format(self.s3_bucket, self.s3_key)
        if self.use_partitioned:
            rendered_partition = self.partition_template.format(**context)
            s3_path = '{}/{}'.format(s3_path, rendered_partition)
             
        if self.json_paths:
            json_paths = f's3://{self.s3_bucket}/{self.json_paths}'
        else:
            json_paths = 'auto'
            
        self.log.info('Coping data from {} to {} on table Redshift'.format(s3_path, self.table))
        formatted_sql = StageToRedshiftOperator.copy_sql.format(
            self.table,
            s3_path,
            credentials.access_key,
            credentials.secret_key,
            json_paths
        )
        redshift.run(formatted_sql)
        self.log.info('Successfully Copied data from {} to {} table on Redshift'.format(s3_path, self.table))

        