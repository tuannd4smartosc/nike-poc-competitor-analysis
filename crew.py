from crewai import Crew
from agents import market_analysis_agent, price_analysis_agent
from tasks import CATasks
import uuid
from config import REPORT_DIR
from utils import generate_file_name, find_files_in_dir, create_pdf_from_md, empty_directory
import uuid
from capture import capture_campaign_snapshot
from email_sender import send_email_with_attachment

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
    uuid_no_special = uuid.uuid4().hex 
    crew = CompetitorAnalysisCrew(company_name, competitors_name, date, uuid_no_special)
    result = crew.run()
    print("result",result)
    marketing_output_file = generate_file_name(uuid_no_special, "marketing", "md")
    pricing_output_file = generate_file_name(uuid_no_special, "pricing", "md")
    marketing_csvs = find_files_in_dir("csv", "marketing")
    pricing_csvs = find_files_in_dir("csv", "pricing")
    print("marketing_csv",marketing_csvs)
    
    marketing_snapshot_paths = capture_campaign_snapshot(marketing_csvs)
    price_snapshot_paths = capture_campaign_snapshot(pricing_csvs)
    
    marketing_pdf_path = create_pdf_from_md(marketing_output_file)
    pricing_pdf_path = create_pdf_from_md(pricing_output_file)
    
    subject = "Test Email with Attachment"
    body = "This is a test email with an attachment sent via Mailtrap."
    from_email = "sender@example.com"  
    to_email = "recipient@example.com"  
    
    file_paths = [*marketing_snapshot_paths, *price_snapshot_paths, marketing_pdf_path, pricing_pdf_path]
    
    send_email_with_attachment(subject, body, from_email, to_email, result, file_paths)
    
    empty_directory("snapshots")
    empty_directory("csv")
    
    return marketing_output_file, pricing_output_file
    
