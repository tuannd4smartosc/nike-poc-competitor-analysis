from crewai import Agent
from textwrap import dedent

# from tools.search_tools import SearchTool
# from tools.shopping_tools import ShoppingTool

from tools.custom_tools import search_tool, shopping_tool

MODEL = "gpt-3.5-turbo"
# MODEL = "gpt-4o"

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