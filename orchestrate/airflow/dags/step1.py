import os
import shutil
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.models.param import Param


def organize_files(date):
    """Organiza os arquivos extraídos para diretórios correspondentes."""
    # Variáveis
    source_dir = "data/dump/"
    base_dir = "data/"
    csv_dir = os.path.join(base_dir, "csv")
    postgres_dir = os.path.join(base_dir, "postgres")

    # Verifica se os diretórios existem
    os.makedirs(csv_dir, exist_ok=True)
    os.makedirs(postgres_dir, exist_ok=True)

    for file_name in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file_name)

        # Ignora se não for um arquivo
        if not os.path.isfile(file_path):
            continue

        # Filtra os arquivos CSV de 'order_details'
        if file_name.startswith("order_details") and file_name.endswith(".csv"):
            destination = os.path.join(csv_dir, date)
        else:
            # Extrai o nome da tabela do nome do arquivo
            table_name = os.path.splitext(file_name)[0]
            destination = os.path.join(postgres_dir, table_name, date)

        # Cria o diretório de destino
        os.makedirs(destination, exist_ok=True)

        # Move o arquivo
        shutil.move(file_path, os.path.join(destination, file_name))
        print(f"Movido: {file_path} -> {os.path.join(destination, file_name)}")


with DAG(
    dag_id="extract_data",
    start_date=datetime(2021, 1, 1),
    catchup=False,
    schedule_interval="@daily",
    params={
        "date": Param(
            default=datetime.now().strftime("%Y-%m-%d"), type="string", format="date"
        )
    }
) as dag:
    # Tarefa para extrair dados do arquivo CSV
    extract_csv = BashOperator(
        task_id="extract_csv",
        bash_command="cd /home/victor/Desktop/TESTE/code-challenge; .meltano/run/bin run tap-csv--order-details target-csv",
    )

    # Tarefa para extrair dados do PostgreSQL
    extract_postgres = BashOperator(
        task_id="extract_postgres",
        bash_command="cd /home/victor/Desktop/TESTE/code-challenge; .meltano/run/bin run tap-postgres target-csv",
    )

    # Tarefa para organizar os arquivos
    organize_folders = PythonOperator(
        task_id="organize_folders",
        python_callable=organize_files,
        op_args=["{{ params.date }}"]
    )

    # Definir a ordem de execução das tarefas
    extract_csv >> extract_postgres >> organize_folders
