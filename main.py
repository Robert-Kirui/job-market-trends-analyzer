from src.data_collection import indeed_scraper, glassdoor_scraper, linkedin_scraper
from src.data_processing import clean_data
from src.analysis import trend_analysis
from src.visualization import dashboard

def main():
    print("Starting Job Market Trends Analyzer...")
    indeed_scraper.scrape_jobs()
    glassdoor_scraper.scrape_jobs()
    linkedin_scraper.scrape_jobs()
    clean_data.process_data()
    trend_analysis.analyze_trends()
    dashboard.launch_dashboard()

if __name__ == "__main__":
    main()
