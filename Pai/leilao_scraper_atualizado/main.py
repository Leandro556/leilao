
from app.scrapers.sc_scraper import scrape_sc
from app.scrapers.rs_scraper import scrape_rs
from app.scrapers.pr_scraper import scrape_pr
from app.database.db import init_db
from app.api.routes import start_api
import threading
import schedule
import time

def run_scrapers():
    print("Iniciando scraping...")
    scrape_sc()
    scrape_rs()
    scrape_pr()
    print("Scraping finalizado.")

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    init_db()
    threading.Thread(target=run_scheduler, daemon=True).start()
    start_api()
