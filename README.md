# scraping_hn


python3 -m venv .venv

source .venv/bin/activate


How to run a workflow (scheduled scraping)
1. prefect cloud login
2. prefect work-pool create my-managed-pool --type prefect:managed
3. python create_deployment.py
4. To manually trigger a deployment, prefect deployment run 'repo-info/my-first-deployment'



How to run DB:
docker build -t my-postgres .
docker run -d --name my-postgres-instance -p 5433:5432 my-postgres
#  my-postgres-instance is name of container, my-postgres is image
