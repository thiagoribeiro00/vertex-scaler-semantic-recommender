from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.vertex_ai.pipeline_job import VertexAIPipelineJobRunOperator

default_args = {
    'owner': 'ikea_ai',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'ikea_recommender_orchestration',
    default_args=default_args,
    description='Orchestrates the Ikea Semantic Recommender Pipeline',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    def validate_data():
        print("Validating data from Olist Source...")

    task_validate = PythonOperator(
        task_id='validate_olist_data',
        python_callable=validate_data,
    )

    # In a real scenario, Airflow triggers the Vertex AI Pipeline
    task_run_vertex_pipeline = VertexAIPipelineJobRunOperator(
        task_id='run_vertex_ai_pipeline',
        display_name='ikea-recommender-run',
        template_path='gs://your-bucket/pipelines/recommendation_pipeline.yaml',
        parameter_values={
            'project_id': 'your-project',
            'location': 'us-central1',
            'index_id': 'your-index',
        },
        project_id='your-project',
        location='us-central1',
    )

    task_validate >> task_run_vertex_pipeline
