# scraping_hn


python3 -m venv .venv

source .venv/bin/activate


How to run a workflow (scheduled scraping)
0. prefect cloud login
0. docker-compose up -d -> run DB, login to pgadmin to see result
1. python main.py -> will run the scraper every day at 6pm
2. prefect deployment run 'scraping/my-hn-deployment' -> manually trigger run


