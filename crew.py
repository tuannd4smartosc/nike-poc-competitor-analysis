from crewai import Crew
from agents import market_analysis_agent, price_analysis_agent
from tasks import CATasks
import uuid
from config import REPORT_DIR
from utils import generate_file_name, find_files_in_dir
import uuid
# from capture import capture_campaign_snapshot
from dotenv import load_dotenv
load_dotenv()


class CompetitorAnalysisCrew:
    def __init__(self, company_name, competitors_name, date_range, id):
        self.company_name = company_name
        self.competitors_name = competitors_name
        self.date_range = date_range
        self.id = id

    def run(self):
        tasks = CATasks()

        research_market_task = tasks.research_market_task(
            market_analysis_agent,
            self.company_name,
            self.competitors_name,
            self.date_range,
            self.id,
        )
        
        analyze_price_task = tasks.analyze_price_task(
            price_analysis_agent,
            self.company_name,
            self.competitors_name,
            self.date_range,
            self.id
        )

        # Define your custom crew here
        crew = Crew(
            agents=[
                market_analysis_agent,
                price_analysis_agent
            ],
            tasks=[
                research_market_task,
                analyze_price_task
            ],
            verbose=True,
        )

        result = crew.kickoff()
        return result
    
    
def run_analysis(company_name, competitors_name, date):
    # uuid_no_special = uuid.uuid4().hex 
    # crew = CompetitorAnalysisCrew(company_name, competitors_name, date, uuid_no_special)
    # result = crew.run()
    # print("result",result)
    # marketing_output_file = generate_file_name(uuid_no_special, "marketing", "md")
    # pricing_output_file = generate_file_name(uuid_no_special, "pricing", "md")
    marketing_csvs = find_files_in_dir("csv", "marketing")
    pricing_csv = find_files_in_dir("csv", "pricing")
    print("marketing_csv",marketing_csvs)
    print("pricing_csv",pricing_csv)
    # return marketing_output_file, pricing_output_file
    
    # capture_campaign_snapshot(marketing_csvs)
