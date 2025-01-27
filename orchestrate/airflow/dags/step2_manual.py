import os
import json
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.models.param import Param

def update_json_paths(date):
    """Essa função verifica se os diretórios existem e, se estiverem presentes, altera o arquivo JSON usado na extração dos CSVs."""
    # Variáveis
    json_file_path = "./json_file.json"
    csv_path = f"data/csv/{date}/"
    postgres_path = f"data/postgres/"

    # Verifica se o diretório de data para CSV existe
    if not os.path.exists(f"data/csv/{date}"):
        print(f"ERRO: O diretório {csv_path} não existe!")
        return  # Interrompe a execução caso não existir
    
    # Verifica se os diretórios base 'csv' e 'postgres' existem
    if not os.path.exists("data/csv") or not os.path.exists("data/postgres"):
        print("ERRO: Os diretórios base 'csv' ou 'postgres' não existem!")
        return  # Interrompe a execução caso não existirem

    # Abrir o arquivo JSON
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Atualizar os caminhos no JSON
    for entry in data:
        entity = entry["entity"]
        file_name = entry["path"].split("/")[-1]  # Pega apenas o nome do arquivo

        # Determina o novo caminho
        if entity == "order_details":
            # Verifica se o diretório específico existe antes de atribuir
            if not os.path.exists(csv_path):
                print(f"ERRO: O diretório {csv_path} não existe para o arquivo {file_name}")
                return  # Interrompe a execução caso o diretório de CSV não existir
            new_path = csv_path + file_name
        else:
            # Verifica se o diretório da tabela dentro de 'postgres' existe
            entity_path = os.path.join(postgres_path, entity)
            if not os.path.exists(entity_path):
                print(f"ERRO: O diretório da tabela {entity_path} não existe para o arquivo {file_name}")
                return  # Interrompe a execução caso não existir

            # Verifica se o diretório da data específica existe dentro da tabela
            entity_date_path = os.path.join(entity_path, date)
            if not os.path.exists(entity_date_path):
                print(f"ERRO: O diretório {entity_date_path} não existe para o arquivo {file_name}")
                return  # Interrompe a execução caso não existir
            new_path = f"{entity_date_path}/{file_name}"

        # Atualiza o caminho no JSON
        entry["path"] = new_path

    # Escreve as alterações de volta no arquivo JSON
    with open(json_file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"Arquivo JSON atualizado com sucesso!")

with DAG(
    dag_id="load_data_manual",
    start_date=datetime(2021, 1, 1),
    catchup=False,
    schedule_interval='@daily',
    params={
        "date": Param(
            default=datetime.now().strftime("%Y-%m-%d"), type="string", format="date"
        )
    }
) as dag:
    # Tarefa para atualizar os caminhos no arquivo JSON
    change_jsonfile = PythonOperator(
        task_id="change_jsonfile_manual",
        python_callable=update_json_paths,
        op_args=["{{ params.date }}"]
    )

    # Tarefa para carregar os dados no Postgres
    load_data = BashOperator(
        task_id="load_data_manual",
        bash_command="cd /home/victor/Desktop/TESTE/code-challenge; .meltano/run/bin run tap-csv target-postgres"
    )

    # Definir a ordem de execução das tarefas
    change_jsonfile >> load_data
