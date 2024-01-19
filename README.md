# scraping_hn


python3 -m venv .venv

source .venv/bin/activate


How to run a workflow (scheduled scraping)
1. prefect cloud login
2. prefect work-pool create my-managed-pool --type prefect:managed
3. python create_deployment.py
4. To manually trigger a deployment, prefect deployment run 'repo-info/my-first-deployment'
