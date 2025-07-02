from datetime import datetime
import random

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator
from airflow.utils.trigger_rule import TriggerRule

def choose_branch():
    # Pick a random float between 0 and 1
    return "branch_high" if random.random() > 0.5 else "branch_low"

with DAG(
    dag_id="random_branching_dag",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["example", "branching"],
) as dag:

    start = EmptyOperator(task_id="start")

    branch = BranchPythonOperator(
        task_id="branch",
        python_callable=choose_branch,
    )

    branch_high = EmptyOperator(task_id="branch_high")
    branch_low = EmptyOperator(task_id="branch_low")

    # A join task that executes regardless of which branch runs
    join = EmptyOperator(
        task_id="join",
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )

    # Define the workflow
    start >> branch
    branch >> branch_high >> join
    branch >> branch_low >> join

