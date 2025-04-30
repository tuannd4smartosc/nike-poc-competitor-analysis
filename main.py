from crewai import Crew
from textwrap import dedent
from agents import market_analysis_agent, price_analysis_agent
from tasks import CATasks
from crew import run_analysis
import uuid

from dotenv import load_dotenv
load_dotenv()

# This is the main function that you will use to run your custom crew.
if __name__ == "__main__":
    print("## Welcome to Competitor Analysis")
    print('-------------------------------')
    company_name = input(
        dedent("""
      What's your company name?
    """))
    date_range = input(
        dedent("""
      What is the date range you are interested in analysing your competitors?
    """))
    run_analysis(company_name, date_range)