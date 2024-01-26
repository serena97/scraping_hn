# Scraping HN with BeautifulSoup and Prefect

This project creates a data pipeline, that scrapes Hacker News every day at 6pm and loads the transformed data into PostgreSQL.

Setting up the environment:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
prefect cloud login


How to run the scheduled scraping:
1. docker-compose up -d -> run DB, login to pgadmin to see result
2. python main.py -> will run the scraper every day at 6pm
3. prefect deployment run 'scraping/my-hn-deployment' -> manually trigger run


