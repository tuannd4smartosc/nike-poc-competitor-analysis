from crewai import Crew, Process
from agents import market_analysis_agent, price_analysis_agent, general_analysis_agent, competitors_detection_agent, swot_analysis_agent, recommendation_agent
from tasks import CATasks
import uuid
from config import REPORT_DIR, MODEL
from utils import generate_file_name, find_files_in_dir, create_pdf_from_md, empty_directory
import uuid
from capture import capture_campaign_snapshot
from email_sender import send_email_with_attachment
from files import read_md_file, combine_md_files

from dotenv import load_dotenv
load_dotenv()


class CompetitorAnalysisCrew:
    def __init__(self, company_name , date_range, id):
        self.company_name = company_name
        self.date_range = date_range
        self.id = id

    def run(self):
        tasks = CATasks()
        
        general_information_task = tasks.general_information_task(
            general_analysis_agent,
            self.company_name,
            self.date_range,
            self.id
        )
        
        competitors_detection_task = tasks.competitor_detection_task(
            competitors_detection_agent,
            self.company_name,
            self.date_range,
            self.id
        )
        
        swot_analysis_task = tasks.swot_analysis_task(
            swot_analysis_agent,
            self.company_name,
            self.date_range,
            self.id,
        )

        research_market_task = tasks.research_market_task(
            market_analysis_agent,
            self.company_name,
            self.date_range,
            self.id,
        )
        
        analyze_price_task = tasks.analyze_price_task(
            price_analysis_agent,
            self.company_name,
            self.date_range,
            self.id,
        )
        
        consultation_task = tasks.consultation_task(
            recommendation_agent,
            self.company_name,
            self.date_range,
            self.id,
        )

        # Define your custom crew here
        crew = Crew(
            agents=[
                general_analysis_agent,
                competitors_detection_agent,
                swot_analysis_agent,
                market_analysis_agent,
                price_analysis_agent,
                recommendation_agent
            ],
            tasks=[
                general_information_task,
                competitors_detection_task,
                swot_analysis_task,
                research_market_task,
                analyze_price_task,
                consultation_task
            ],
            verbose=True,
        )

        result = crew.kickoff()
        return result
    
    
def run_analysis(company_name, date):
    uuid_no_special = uuid.uuid4().hex 
    crew = CompetitorAnalysisCrew(company_name, date, uuid_no_special)
    crew.run()
    
    output_md = combine_md_files(REPORT_DIR, "final_reports")
    final_pdf_path = create_pdf_from_md(output_md)
    
    marketing_csvs = find_files_in_dir("csv", "marketing")
    
    marketing_snapshot_paths = capture_campaign_snapshot(marketing_csvs)
    
    subject = "Test Email with Attachment"
    body = "This is a test email with an attachment sent via Mailtrap."
    from_email = "sender@example.com"  
    to_email = "recipient@example.com"  
    
    file_paths = [*marketing_snapshot_paths, final_pdf_path]
    
    send_email_with_attachment(subject, body, from_email, to_email, read_md_file(output_md), file_paths)
    
    empty_directory("snapshots")
    empty_directory("csv")
    empty_directory("reports")
    
    return output_md
    
