from crewai import Agent
from textwrap import dedent
from tools.custom_tools import search_tool, shopping_tool
from config import MODEL

general_analysis_agent = Agent(
    role="Competitor Analysis Report Writer",
    backstory=dedent(
        f"""Expert in writing executive summary, market research and specialised in sportwear industry."""),
    goal=dedent(f"""
                Write an executive summary and overview of the sportwear industry.
                """),
    tools=[
        search_tool,
    ],
    allow_delegation=False,
    verbose=True,
    llm=MODEL,
    max_iter=3
)

competitors_detection_agent = Agent(
    role="Competitor Detection Agent",
    backstory=dedent(
        f"""Expert in finding basic information from big sportwear companies."""),
    goal=dedent(f"""
                Create a detailed basic information report for top three sportwear companies.
                """),
    tools=[
        search_tool,
    ],
    allow_delegation=False,
    verbose=True,
    llm=MODEL,
    max_iter=3
)

swot_analysis_agent = Agent(
    role="SWOT Analysis Expert Agent",
    backstory=dedent(
        f"""Expert in SWOT analysis from big sportwear companies."""),
    goal=dedent(f"""
                Create a detailed SWOT analysis report for big sportwear companies.
                """),
    tools=[
        search_tool,
    ],
    allow_delegation=False,
    verbose=True,
    llm=MODEL,
    max_iter=3
)

market_analysis_agent = Agent(
    role="Expert Market Analysis Agent",
    backstory=dedent(
        f"""Expert in finding active promotion campaigns from big sportwear companies."""),
    goal=dedent(f"""
                Create a detailed promotion campaigns for three sportwear companies with clear explanations on how the campaigns would impact on the companies.
                """),
    tools=[
        search_tool,
    ],
    allow_delegation=False,
    verbose=True,
    llm=MODEL,
    max_iter=3
)

price_analysis_agent = Agent(
    role="Expert Price Analysis Agent",
    backstory=dedent(
        f"""Expert in analysing pricing strategy from big sportwear companies regard price, discounts, and ratings."""),
    goal=dedent(f"""
                Create a detailed pricing analysis for three sportwear companies with clear explanations on how the campaigns would impact on the companies.
                """),
    tools=[
        search_tool,
    ],
    allow_delegation=False,
    verbose=True,
    llm=MODEL,
    max_iter=3
)

recommendation_agent = Agent(
    role="Business Consultant Expert",
    tools=[
        search_tool,
    ],
    backstory=dedent(
        f"""Seasoned consultation expert with strong understanding about the sportwear market"""),
    goal=dedent(f"""
                Create a recommendation guide for a business to stand out from its competitors.
                """),
    allow_delegation=False,
    verbose=True,
    llm=MODEL,
    max_iter=3
)