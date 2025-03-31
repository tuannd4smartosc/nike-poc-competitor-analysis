from crewai import Task
from textwrap import dedent
from utils import generate_file_name

class CATasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def general_information_task(self, agent, company_name, date, id):
        return Task(
            description=dedent(
                f"""
                    **Task**: Develop an overview of the sportwear market and {company_name}
                    **Description**: 
                        Give an executive summary about the sportwear market
                        Give an overview about {company_name} most recent news
                        Analyse the market position of {company_name} in the sportwear market
                        Give an overview of {company_name} opportunities and challenges
                    **Parameters**: 
                    - Date range: {date}

                    **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            output_file=generate_file_name(id, "0_intro", "md"),
            expected_output=f"""
            An executive summary about the sportswear industry and {company_name}'s newest news.
            A comprehensive analysis about the market position of {company_name} in the sportwear industry.
            An overview of {company_name}'s opportunities and challenges.
            """
        )

    def competitor_detection_task(self, agent, company_name, date, id):
        return Task(
            description=dedent(
                f"""
                    **Task**: Develop a general research about {company_name}'s top 3 competitors in the given date range. 
                    **Description**: 
                        The task must include a list of bullet points comparing the company name, website url, founded, headquarters, market share, revenue, number of employees, and key products.
                    **Parameters**: 
                    - Date range: {date}

                    **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            output_file=generate_file_name(id, "1_competitors", "md"),
            expected_output=f"""
            A markdown report with detailed research findings of the following competitors, including the following categories for each competitor:
                - Company Name.
                - Website url.
                - Foundded.
                - Headquarters.
                - Market Share.
                - Revenue.
                - Number of Employees.
                - Key Products.
            """
        )
        
    def swot_analysis_task(self, agent, company_name, date, id, context = []):
        return Task(
            description=dedent(
                f"""
                    **Task**: Develop a SWOT Analysis about the {company_name}'s competitors versus {company_name} in the given date range.
                    **Description**: 
                        The task must be a markdown report with detailed SWOT analysis for Nike versus the given competitors.
                        The task must highlight on key information that impacts on {company_name}'s performance.
                    **Parameters**: 
                    - Date range: {date}

                    **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            output_file=generate_file_name(id, "2_swot", "md"),
            context=context,
            expected_output=f"""A markdown report starts with a SWOT Analysis table analyzing {company_name} versus its competitors:
                - Strengths: [List key strengths in full sentence]
                - Weaknesses: [List key weaknesses in full sentence]
                - Opportunities: [List potential opportunities in full sentence]
                - Threats: [List potential threats in full sentence]
            """
        )

    def research_market_task(self, agent, company_name, date, id, context = []):
        return Task(
            description=dedent(
                f"""
                    **Task**: Develop a promotion campaign analysis for {company_name}'s competitors in the given date range.
                    **Description**: 
                        Search and analyze recent promotion campaigns from {company_name}'s competitors and their impacts to {company_name}.
                        The task must also summarize in detailed each ad campaign from each company, and the impact of each campaign on its competitors.
                        The final report must be a markdown report with detailed analysis on ad campaigns and impacts on each company.

                    **Parameters**: 
                    - Date range: {date}

                    **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            context=context,
            output_file=generate_file_name(id, "3_marketing", "md"),
            expected_output=f"""
            A markdown report of {company_name}'s competitors' promotion campaigns. The report must have the following key points:
            - Campaign summary: Summary of each promotion campaign.
            - Campaign results: How the campaign improves the company's performance.
            - Campaign impacts on {company_name}: How each campaign would impact on {company_name}
            """
        )
        
    def analyze_price_task(self, agent, company_name, date, id, context = []):
        return Task(
            description=dedent(
                f"""
                    **Task**: Develop a product/pricing analysis for {company_name} and {company_name}'s competitors in the given date range:
                    **Description**: 
                        - The task must analyze each competitor's product and pricing strategy and how they are dealing with the current market trend.
                        - The task must include a table that compares each company's key products, unique selling point, pricing, rating, and justification about the comparison.
                        - The task must comment on the comparison and make analysis on how the competitors' pricing strategy would impact on {company_name}
                    **Parameters**: 
                    - Date range: {date}

                    **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            context=context,
            output_file=generate_file_name(id, "4_pricing", "md"),
            expected_output=f"""
                A brief introduction about the pricing analysis.
                A table including the following columns:
                - Company name
                - Pricing
                - Quality
                - Ratings
                - Unique Selling Point
                - Key Insights
                
                Do not include a conclusion.
            """
        )
        
    def consultation_task(self, agent, company_name, date, id, context = []):
        return Task(
            description=dedent(
                f"""
                    **Task**: Develop a comprehensive guide for {company_name} to stand out from its competitors:
                    **Description**: 
                        - Give a conclusion on the performance of {company_name}'s competitors.
                        - Analyse the market positioning of {company_name}
                        - Provide a detailed action plan for {company_name} to follow to increase its market share, sales revenue and stand out from its competitors.
                        - Construct a sales revenue forecast for {company_name} in the next five years.
                    **Parameters**: 
                    - Date range: {date}

                    **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            context=context,
            output_file=generate_file_name(id, "5_consultation", "md"),
            expected_output=f"""
                A detailed consultation guide including the following points:
                - Conclusion: Conclusion of {company_name} competitors' performance.
                - Market positioning: Analyse the market positioning of {company_name}
                - Next actions: Next actions plan for {company_name} to follow
                - Sales forecast: Sales revenue forecast for {company_name}
            """
        )