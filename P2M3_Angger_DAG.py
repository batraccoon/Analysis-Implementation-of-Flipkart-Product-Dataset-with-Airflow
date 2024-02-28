'''
=================================================
Milestone 3

Name  : Angger Rizky Firdaus
Batch : HCK-012

This program is designed to automate the transformation and loading of data from PostgreSQL to ElasticSearch. The dataset used is sourced from E-commerce companies Flipkart and Amazon.
=================================================
'''


#load Libarry
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime
from sqlalchemy import create_engine #koneksi ke postgres
import pandas as pd
from datetime import timedelta

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

    
#Function for Get Table from SQL to CSV
def ambil_data():
    '''
    This function is used to connect Airflow processes to PostgreSQL. It requires the database name, username, password, and host.
    '''
    # fetch data
    database = "airflow_m3"
    username = "airflow_m3"
    password = "airflow_m3"
    host = "postgres"

    # Make URL to connect Postgree
    postgres_url = f"postgresql+psycopg2://{username}:{password}@{host}/{database}"

    # Use this URL when establishing a SQLAlchemy connection.
    engine = create_engine(postgres_url)
    conn = engine.connect()

    #saving CSV from postgre database
    df = pd.read_sql_query("select * from table_m3", conn) #nama table sesuaikan sama nama table di postgres
    df.to_csv('/opt/airflow/dags/P2M3_Angger_data.csv', sep=',', index=False)
    

#Preprocessing column to clean the dataset
def preprocessing(): 
    ''' 
    The function to clean data involves several steps. It includes converting column names to lowercase, renaming columns, dropping null and duplicate values, and changing data types as needed.
    '''
    # data loading
    data = pd.read_csv("/opt/airflow/dags/P2M3_Angger_data.csv")

    #syntax for making column name lower case 
    col = []
    for x in data.columns:
        col.append(x.lower())
    data.columns = col

    # rename column name 
    data.rename(columns = {'maincateg':'main_category', 'price1':'price', 
                              'actprice1':'act_price',
                              'offer %':'discount_percent',
                              'norating1':'no_rating',
                              'noreviews1':'no_reviews',
                              'star 5f':'5_star_rating',
                              'star 4f':'4_star_rating',
                              'star 3f':'3_star_rating',
                              'star 2f':'2_star_rating',
                              'star 1f':'1_star_rating',
                              'fulfilled1':'fulfilled'}, inplace = True)
    #drop null and duplicates
    data.dropna(inplace=True)
    data.drop_duplicates(inplace=True)
    #change datatype
    data['5_star_rating'] = data['5_star_rating'].astype('int64')
    data['4_star_rating'] = data['4_star_rating'].astype('int64')
    data['3_star_rating'] = data['3_star_rating'].astype('int64')
    data['discount_percent'].replace('%','', regex=True, inplace=True)
    data['discount_percent'] = data['discount_percent'].astype('float')
    data['no_rating'] = data['no_rating'].astype('int64')
    #data saving
    data.to_csv('/opt/airflow/dags/P2M3_Angger_data_clean.csv', index=False)
    
#Upload Clean CSV to ElasticSearch   
def upload_to_elasticsearch():
    ''' 
    This function serves to upload a CSV file to the Elasticsearch system.
    '''
    es = Elasticsearch("http://elasticsearch:9200")
    df = pd.read_csv('/opt/airflow/dags/P2M3_Angger_data_clean.csv')
    
    for i, r in df.iterrows():
        doc = r.to_dict()  # Convert the row to a dictionary
        res = es.index(index="table_m3", id=i+1, body=doc)
        print(f"Response from Elasticsearch: {res}")
        
#Setting        
default_args = {
    'owner': 'Angger', 
    'start_date': datetime(2024, 2, 22, 17, 00)- timedelta(hours=7)
}

#Workflow
with DAG(
    "P2M3_Angger_DAG_hck", #atur sesuai nama project kalian
    description='Milestone_3',
    schedule_interval='30 6 * * *', #atur schedule untuk menjalankan airflow pada 06:30.
    default_args=default_args, 
    catchup=False
) as dag:
    # task: 1
    ambil_data_pg = PythonOperator(
        task_id='ambil_data_postgres',
        python_callable=ambil_data) #
    

    # Task: 2
    '''  Fungsi ini ditujukan untuk menjalankan pembersihan data.'''
    edit_data = PythonOperator(
        task_id='edit_data',
        python_callable=preprocessing)

    # Task: 3
    upload_data = PythonOperator(
        task_id='upload_data_elastic',
        python_callable=upload_to_elasticsearch)

    #The process to execute it in Airflow 
    ambil_data_pg >> edit_data >> upload_data



