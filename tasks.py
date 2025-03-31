from crewai import Task
from textwrap import dedent
from utils import generate_file_name

class CATasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def general_information_task(self, agent, company_name, competitors_name, date, id):
        return Task(
            description=dedent(
                f"""
                    **Task**: Develop a general research about the following companies: {competitors_name}
                    **Description**: 
                        {competitors_name} are big competitors of {company_name}.
                        The task must start with an introduction about {competitors_name}.
                        The task must include a list of bullet points comparing the company name, website url, founded, headquarters, market share, revenue, number of employees, and key products.
                    **Parameters**: 
                    - Companies: {competitors_name}

                    **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            output_file=generate_file_name(id, "background", "md"),
            expected_output=f"""A markdown report starts with an introduction, and then detailed research findings the following companies, including the following categories {company_name}
                1. Company Name.
                2. Website url.
                3. Foundded.
                4. Headquarters.
                5. Market Share.
                6. Revenue.
                7. Number of Employees.
                8. Key Products.
                
                Do not include a conclusion.
            """
        )
        
    def swot_analysis_task(self, agent, company_name, competitors_name, date, id):
        return Task(
            description=dedent(
                f"""
                    **Task**: Develop a SWOT Analysis for the following companies: {competitors_name}
                    **Description**: 
                        {competitors_name} are big competitors of {company_name}.
                        
                    **Parameters**: 
                    - Companies: {competitors_name}

                    **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            output_file=generate_file_name(id, "background", "md"),
            expected_output=f"""A markdown report starts with an introduction, and then detailed research findings the following companies, including the following categories {company_name}
                1. Company Name.
                2. Website url.
                3. Foundded.
                4. Headquarters.
                5. Market Share.
                6. Revenue.
                7. Number of Employees.
                8. Key Products.
                
                Do not include a conclusion.
            """
        )

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
            expected_output=f"A markdown report with detailed analysis of ad campaigns, their impacts on each company, and next actions for {company_name}."
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
            expected_output=f"A markdown report with detailed analysis of pricing strategies, impacts on each company and next actions for {company_name}."
        )