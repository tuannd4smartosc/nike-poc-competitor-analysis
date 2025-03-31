from crewai import Agent
from textwrap import dedent

# from tools.search_tools import SearchTool
# from tools.shopping_tools import ShoppingTool

from tools.custom_tools import search_tool, shopping_tool

MODEL = "gpt-3.5-turbo"
# MODEL = "gpt-4o"

general_analysis_agent = Agent(
    role="General Competitor Analysis Agent",
    backstory=dedent(
        f"""Expert in finding background information from big sportwear companies."""),
    goal=dedent(f"""
                Create a detailed background information report for five sportwear.
                """),
    tools=[
        search_tool,
    ],
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
    verbose=True,
    llm=MODEL,
    max_iter=3
)

market_analysis_agent = Agent(
    role="Expert Market Analysis Agent",
    backstory=dedent(
        f"""Expert in finding active promotion campaigns from big sportwear companies."""),
    goal=dedent(f"""
                Create a detailed promotion campaigns for five sportwear companies with clear explanations on how the campaigns would impact on the companies.
                """),
    tools=[
        search_tool,
    ],
    verbose=True,
    llm=MODEL,
    max_iter=3
)

price_analysis_agent = Agent(
    role="Expert Price Analysis Agent",
    backstory=dedent(
        f"""Expert in analysing pricing strategy from big sportwear companies regard price, discounts, and ratings."""),
    goal=dedent(f"""
                Create a detailed pricing analysis for five sportwear companies with clear explanations on how the campaigns would impact on the companies.
                """),
    tools=[
        shopping_tool,
    ],
    verbose=True,
    llm=MODEL,
    max_iter=3
)