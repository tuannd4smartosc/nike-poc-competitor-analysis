from crewai import Task
from textwrap import dedent
from utils import generate_file_name

class CATasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def research_market_task(self, agent, company_name, competitors_name, date, id):
        return Task(
            description=dedent(
                f"""
                    **Task**: Develop a market analysis for {company_name}'s competitors: {competitors_name}
                    **Description**: 
                        Search and analyze recent promotion campaigns from {competitors_name}
                        and their impacts to {company_name}.
                        The task must also summarize in detailed each ad campaign from each company, and the impact of each campaign on its competitors.
                        The final report must be a markdown report with detailed analysis on ad campaigns and impacts on each company.

                    **Parameters**: 
                    - My company: {company_name}
                    - My competitors: {competitors_name}
                    - Date range: {date}

                    **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            output_file=generate_file_name(id, "marketing", "md"),
            expected_output="A markdown report with detailed analysis of ad campaigns and their impacts on each company."
        )
        
    def analyze_price_task(self, agent, company_name, competitors_name, date, id):
        return Task(
            description=dedent(
                f"""
                    **Task**: Develop a pricing analysis for {company_name}'s competitors: {competitors_name}
                    **Description**: 
                        Search and analyze recent pricing strategy, including price, discounts, ratings, from {competitors_name}
                        and their impacts to {company_name}.
                        The task must include a table comparing the price, discounts, and ratings among {competitors_name}.
                        The final report must be a markdown report with detailed analysis and a table comparing {competitors_name} pricing strategy.

                    **Parameters**: 
                    - My company: {company_name}
                    - My competitors: {competitors_name}
                    - Date range: {date}

                    **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            output_file=generate_file_name(id, "pricing", "md"),
            expected_output="A markdown report with detailed analysis of pricing strategies and their impacts on each company."
        )