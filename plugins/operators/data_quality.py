from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    """Custom Operator for performing data quality check on a table.
    
    Attributes:
        ui_color (str): color code for task in Airflow UI.
        count_template (str): template string for checking if table contains data.
        
    """
    ui_color = '#89DA59'
    count_template = """
                     SELECT COUNT(*) 
                     FROM {}"""

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 dq_checks=[],
                 *args, **kwargs):
        """Initializes a Data Quality Check Operator.
        Args:
            redshift_conn_id (str): Airflow connection ID for redshift database.
            table (str): Name of table to quality check.
            query (:obj:`str`, optional): Query use for testing table quality.
            result (:obj:`str`, optional): Expected result

        """
        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.dq_checks = dq_checks

    def execute(self, context):
        """Executes task for data quality check.
        Args:
            context (:obj:`dict`): Dict with values to apply on content.
            
        """
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.log.info(f'Fetching Record count from {self.table}...')
        records = redshift.get_records(DataQualityOperator.count_template.format(self.table))
        
        self.log.info(f'Checking if {self.table} table contains returned results...')
        if len(records) < 1 or len(records[0]) < 1:
            raise ValueError(f'Fail: No results for {self.table} table')
            
        self.log.info(f'Checking if {self.table} table has records...')
        num_records = records[0][0]
        if num_records < 1:
            raise ValueError(f'Fail: 0 rows in {self.table} table')
        self.log.info(f'Has {records[0][0]} Records!')
        
        failing_tests = []
        error_count = 0

        for check in self.dq_checks:
            sql = check.get('check_sql')
            exp_result = check.get('expected_result')

            records = redshift.get_records(sql)[0]

            if exp_result != records[0]:
                error_count += 1
                failing_tests.append(sql)

        if error_count > 0:
            self.log.info('Tests failed')
            self.log.info(failing_tests)
            raise ValueError('Data quality check failed')
       
        self.log.info(f'Data Quality Check on {self.table} table was successful!')