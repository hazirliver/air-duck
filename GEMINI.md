# Project Air-Duck: Technical Specification and Architecture

This document outlines the technical specifications, architecture, and operational procedures for the Air-Duck project.

## 1. Project Overview

The project aims to build and operate a data processing pipeline on the Nebius cloud platform. The pipeline will leverage Kubernetes for orchestration, Airflow for workflow management, and a suite of Nebius managed services for storage and data warehousing. The core of the data architecture is a data lake built with DuckLake on top of an S3-compatible object store, versioned by LakeFS.

## 2. Core Technologies

- **Orchestrator:** Apache Airflow
- **Container Orchestrator:** Nebius Managed Kubernetes (K8s)
- **Task Operator:** `KubernetesPodOperator`
- **Container Registry:** Nebius Container Registry
- **Raw Data Store:** Nebius Object Storage (S3-compatible)
- **Data Versioning:** LakeFS
- **Data Lake Engine:** DuckLake
- **Structured Data Store:** Nebius Managed PostgreSQL
- **Dependency Management:** `uv`

## 3. Architecture

The architecture is designed as a series of containerized tasks orchestrated by Airflow running on a Kubernetes cluster.

1.  **Airflow & Kubernetes:** Airflow is deployed within the Nebius Managed Kubernetes cluster. DAGs primarily use the `KubernetesPodOperator` to launch individual pods for each task. This ensures that each task runs in a clean, isolated, and reproducible environment with its own specific dependencies.

2.  **Container Images:** Each task pod is defined by a Docker image. These images are built and pushed to the Nebius Container Registry. The `KubernetesPodOperator` pulls the required image from the registry at runtime.

3.  **Data Ingestion & Raw Storage:** Raw data is ingested and stored in a bucket within Nebius Object Storage.

4.  **Data Versioning with LakeFS:** A LakeFS repository is layered on top of the raw data bucket in Nebius Object Storage. This provides Git-like version control for the data, enabling atomic commits, branching, and rollbacks. This is crucial for data quality and reproducibility.

5.  **Data Processing & The Data Lake:**
    -   Airflow tasks (running as pods) process the raw data.
    -   The processed, structured data is managed by **DuckLake**. DuckLake uses the versioned object storage as its foundation, creating a high-performance data lake.

6.  **Structured Storage:** Final, aggregated, or mission-critical results are loaded into a Nebius Managed PostgreSQL database for serving, analytics, or use by other applications.

## 4. Project Structure

The project is organized into the following directories:

-   `.github/workflows/`: CI/CD pipelines (e.g., for testing, building images, deploying infrastructure).
-   `tests/`: Contains project tests.
    -   `integration/`: Integration tests for external services.
-   `build/`: Contains build-related artifacts.
    -   `docker/`: Dockerfiles for building container images.
        -   `base/`: Base images with common dependencies.
        -   `processing/`: Images for specific data processing tasks.
    -   `scripts/`: Build-related scripts.
-   `data/`: Local data storage and configuration.
    -   `ducklake/`: Configuration and local files for DuckLake.
    -   `lakefs/`: Configuration for LakeFS.
-   `infra/`: Infrastructure as Code (IaC).
    -   `kubernetes/`: Kubernetes manifests and Helm charts.
        -   `helm/`: Helm chart values for applications like Airflow and LakeFS.
            -   `airflow/`: Values for the Airflow Helm chart.
            -   `lakefs/`: Values for the LakeFS Helm chart.
        -   `manifests/`: Raw Kubernetes manifests.
    -   `terraform/`: Terraform scripts for managing Nebius infrastructure.
        -   `environments/`: Environment-specific configurations (dev, prod).
            -   `dev/`: Development environment configuration.
            -   `prod/`: Production environment configuration.
        -   `modules/`: Reusable Terraform modules.
-   `scripts/`: General-purpose scripts for automation.
-   `airflow/`: Airflow-specific files.
    -   `dags/`: Airflow DAG definitions.
    -   `plugins/`: Custom Airflow plugins.
    -   `config/`: Airflow configuration files.
-   `.env`: Stores environment variables, including credentials for Nebius services, LakeFS, and PostgreSQL. It also includes the S3 path and endpoint URL.
-   `.gitignore`: Standard Git ignore file.
-   `.python-version`: Specifies the Python version.
-   `main.py`: Main application entry point.
-   `metadata.ducklake`: DuckLake metadata file.
-   `pyproject.toml`: Project dependencies for `uv`.
    -   **Core Dependencies:** `duckdb`, `pyarrow`, `boto3`, `lakefs-client`, `psycopg`, `apache-airflow`, `apache-airflow-providers-cncf-kubernetes`
    -   **Development Dependencies:** `ruff`
-   `README.md`: General project documentation.
-   `uv.lock`: Lockfile for reproducible builds.
