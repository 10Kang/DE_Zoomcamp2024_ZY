## Date Engineering ZoomCamp 2024 &#128640;
The [DE Zoomcamp cohort 2024](https://github.com/DataTalksClub/data-engineering-zoomcamp) is organized by [DataTalksClub](https://github.com/DataTalksClub). 

* [Module 1: Dockers and Terraform](./module_1_docker_terraform) &#128230;

  - Run postgres and pgadmin in containers. Best practice for reproducibility
  - Infrastructure as Code (Terraform).

  - Service account in GCP: credentials as .json file in project directory.

* [Module 2: Data Orchestration - Mage](./module_2_mage_zoomcamp) &#128295;
  
    - Mage as the main tools for data orchestration
    - Directly git clone from the [Mage repository for DE Zoomcamp 2024](https://github.com/mage-ai/mage-zoomcamp)
    - Run containers to set up the mage application
    ```
    docker compose build 
    docker compose up
    ```
* [Module 3: Data Warehouse & Big Query](./module_3_data_warehouse_bigquery) &#127981;

  - Data Warehouse (Big Query) for OLAP
  - External Table vs Materialized Table
  - Optimization of Query to increase performance and save cost via partitioning and clustring.

* [Module 4: Analytics Engineering with dbt](./module_4_analytic_engineering_dbt/) &#128202;
  
  - Check out the medium article by me at below

  - [What is DBT and how to integrate it with BigQuery ? 🚀](https://medium.com/@kangzhiyong1999/what-is-dbt-and-how-to-integrate-it-with-bigquery-e7b3db7241ef)
  - [From Testing/Documenting of dbt model to deployment in dbt cloud 🚀](https://medium.com/@kangzhiyong1999/from-testing-documenting-of-dbt-model-to-deployment-in-dbt-cloud-a6481c50aa64)