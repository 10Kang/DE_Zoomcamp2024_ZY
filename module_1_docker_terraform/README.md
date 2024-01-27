# Notes on module 1 from DE ZoomCamp 2024

- 💭  Docker :  A refresher to strengthen understanding on containers, e.g. enabling the talking between containers via network or docker-compose 📦 

 - 💭  Data Ingestion with Python : Data Definition Language (DDL) can be called directly using Pandas module 🤙 

 - 💭  SQL Query: Don't forget the basic query concept or strategy to answer the business problem 🚕  

 - 💭  Terraform: Infrastructure as Code (IaC). Fairly self-explanatory 💻

 - 💭  GCP: Connecting to cloud computation power; managing BigQuery and cloud storage bucket using service account 🖥  


## Command to run containers seperately

- TO run postgres in docker
```
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \ 
  -p 5432:5432 \ 
  postgres:13

```

- To run PgAdmin4 in docker 

```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4
```

  ## We need to configure a network to allow communication of postgres and pgadmin

- Prior running any containers, remember to set up network

```bash
docker network create pg-network

```

- To run postgres with network

```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \ 
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database
  postgres:13
```

- To run pgadmin with network 

```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

## Homework for ingestion of green taxi data
We use the dockerize ingestion method by specifiy the network configuration in the [docker-compose.yaml](docker-compose.yaml) file which use the previous network that have been created. Upon the running the command of "docker-compose up". You can check your container is in the network or not using the code below. And you will see two containers in the same network

```bash
docker network inspect pg-network
```

To allow the dockerize ingestion, we then have to build a new image with new upload.py (ingestion.py as refer in the modules) from [Dockerfile](Dockerfile)

```bash
docker build -t taxi_ingest:v001 .
```

After running the command above, have the code below and the ingestion will be done automatically in bash terminal

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"

docker run -it --network=pg-network \
  green_taxi_ingest:v001 \
  --user=root \
  --password=root \
  --host=pgdatabase \
  --port=5432 \
  --db=ny_taxi \
  --table_name='green_taxi_trips' \
  --url=${URL} 

```

## The SQL Query for Homework

To get the answer of homework question 3 to 6, you can refer to [homework1.sql](homework1.sql)

## Terraform (Infrastucture as Code)

The variables.tf file location is set to the region nearest to me to ensure lower latency and no multiple region is enabled to save cost.

  - To run initiate terraform for project
  ```bash
  terraform init
  ```
  - To execulte plan of terraform: main.tf
  ```bash
  terraform plan
  ```
  - To apply to see what service will be initiated in GCP
  ```bash
  terraform apply
  ```
  - To destroy allt the resources after getting the job done to save cost
  ```bash
  terraform destroy
  ```