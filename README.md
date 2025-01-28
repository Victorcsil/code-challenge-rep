# Relatório - Code Challenge ED

## Introdução
Este relatório documenta a solução desenvolvida para o **Code-Challenge for Software Developer** da Indicium. O projeto consiste na implementação de um pipeline de dados utilizando **Meltano**, **Airflow** e **PostgreSQL**. O Airflow foi responsável por orquestrar as etapas do pipeline, que incluem:

- Extração de dados de duas fontes: um banco **PostgreSQL Northwind** e um arquivo **CSV (order_details)**.
- Armazenamento local dos dados em diretórios organizados por fonte, tabela e data.
- Carregamento final dos dados em um banco **PostgreSQL** preparado para análises e relatórios.

---

## Ideia de Solução
A solução foi projetada com um pipeline dividido em três etapas principais:

1. **Extração:** 
   - Dados extraídos do banco **PostgreSQL Northwind** usando o `tap-postgres`.
   - Dados do arquivo **CSV** `order_details` extraídos usando o `tap-csv`.

2. **Armazenamento:** 
   - Os dados extraídos foram salvos localmente em arquivos **CSV** utilizando o `target-csv`, organizados por fonte, tabela e data.

3. **Carregamento:** 
   - Os arquivos gerados foram carregados no banco **PostgreSQL final** utilizando o `target-postgres`.

A orquestração do pipeline foi realizada pelo **Airflow** que foi configurado via meltano utility. O Airflow foi responsável por coordenar as etapas com DAGs específicas para extração e carregamento.


---

### Configuração do Meltano e Seleção de Plugins
Os seguintes plugins foram selecionados para o Meltano:

- **Extractors:**
  - `tap-csv`: Para lidar com o arquivo `order_details.csv`.
  - `tap-postgres`: Para extrair dados do banco **PostgreSQL Northwind**.

- **Loaders:**
  - `target-csv`: Para armazenar os dados extraídos em formato CSV.
  - `target-postgres`: Para carregar os dados no banco **PostgreSQL** final.

---

### Orquestração com Airflow
A orquestração foi implementada utilizando a **utility do Airflow** fornecida pelo Meltano. Esta abordagem foi escolhida para manter o projeto simples e de fácil configuração.

---

# Passo a Passo para Executar o Projeto

Esse projeto foi feito no Ubuntu 22.04 com python3.11, e pode não ser suportado em outras versões ou sistemas operacionais.

# Passo a Passo para Configuração e Execução do Projeto

### 1. Clonar o Repositório

1. Clone o repositório do projeto:
   - `git clone https://github.com/Victorcsil/code-challenge-rep.git`
2. Acesse a pasta do projeto:
   - `cd code-challenge-rep`

---

### 2. Criar e Ativar o Ambiente Virtual

1. Crie um ambiente virtual:
   - `python3.11 -m venv .venv`
2. Ative o ambiente virtual:
   - **No Linux/Mac:** `source .venv/bin/activate`
   - **No Windows:** `.venv\Scripts\activate`

---

### 3. Instalar Dependências

Com o ambiente virtual ativo, instale as dependências listadas no arquivo `requirements.txt`:
   - `pip install -r requirements.txt`

---

### 4. Instalar Plugins do Meltano

Instale os plugins necessários para o Meltano:
   - `meltano install`

---

### 5. Iniciar os Serviços com Docker Compose

Suba os serviços necessários para a execução do projeto:
   - `docker-compose up -d`

---

### 6. Configurar as Senhas dos Conectores

1. Configure a senha para o conector `tap-postgres`:
   - `meltano config tap-postgres set password thewindisblowing`
2. Configure a senha para o conector `target-postgres`:
   - `meltano config target-postgres set password dbfinalpassword`

---

### 7. Inicializar o Airflow

Inicie o Airflow:
   - `meltano invoke airflow`

---

### 8. Criar um Usuário Administrador no Airflow

Crie um usuário administrador para acessar o Airflow:
   - `meltano invoke airflow users create -u admin -p password --role Admin -e admin -f admin -l admin`

---

### 9. Iniciar o Scheduler e o Webserver do Airflow

1. Inicie o scheduler do Airflow:
   - `meltano invoke airflow scheduler`
2. Em outro terminal, com o ambiente virtual ainda ativo, execute novamente o comando para iniciar o webserver:
   - `meltano invoke airflow webserver`

---

### 10. Acessar a Interface do Airflow

Abra o navegador e acesse:

**[http://localhost:8080](http://localhost:8080)**

Faça login com as credenciais configuradas:
- **Usuário:** `admin`
- **Senha:** `password`

O pipeline está pronto para ser executada!

# Assinatura

Desenvolvido por: [Victor Castro Silva](https://www.linkedin.com/feed/)
JAN 2025

