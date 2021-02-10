# -*- coding: UTF-8 -*-

"""
Main file for implementing the Data Workflow
"""

# import from standard library
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# project imports
from servier.clean import clean_clinical_trials, clean_drugs, clean_pubmed
from servier.process import drug_mention_pubmed, drug_mention_clinical_trial
from servier.process import merge_pubmed_clinical_trial

default_args = {
        "start_date": datetime(2021, 2, 6)}

dag = DAG(dag_id="my_dag",
          description="ELT Workflow for drug mention in scientific reviews",
          default_args=default_args)


# First step: Cleaning data

clean1 = PythonOperator(task_id="clean_pubmed",
                        python_callable=clean_pubmed,
                        dag=dag)

clean2 = PythonOperator(task_id="clean_clinical_trials",
                        python_callable=clean_clinical_trials,
                        dag=dag)

clean3 = PythonOperator(task_id="clean_drugs",
                        python_callable=clean_drugs,
                        dag=dag)


# Second step: Compute drug search on Medical publication and clinical trials

process1 = PythonOperator(task_id="drug_mention_pubmed",
                          python_callable=drug_mention_pubmed,
                          dag=dag)

process2 = PythonOperator(task_id="drug_mention_clinical_trial",
                          python_callable=drug_mention_clinical_trial,
                          dag=dag)

# Third step: merge both outputs

process3 = PythonOperator(task_id="merge",
                          python_callable=merge_pubmed_clinical_trial,
                          dag=dag)

# task hierarchy

process1 << [clean1, clean3]
process2 << [clean2, clean3]
process3 << [process1, process2]
