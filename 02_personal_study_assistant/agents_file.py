from agents import Agent
from tools import web_search

summarizer_agent = Agent(
    name="KnowledgeSummarizerAgent",
    instructions=(
        "You are a Summarization Agent. Your task is to read through the research content "
        "(text, links, or excerpts) handed off to you and extract the most important information. "
        "Condense the content into clear, easy-to-read bullet points or short paragraphs. "
        "Focus on simplifying complex ideas, ensuring clarity and relevance to the original study topics. "
        "Return a concise summary that makes the content easier to understand and review."
    ),
)

research_agent = Agent(
    name="TopicResearchAgent",
    instructions=(
        "You are a Research Assistant Agent. When a user provides study topics, use the `web_search` tool"
        "to find credible, high-quality resources (e.g., academic articles, videos, blogs, documentation). "
        "Return a list of resources for each topic, including titles, short descriptions, and direct URLs. "
        "Once research is gathered, automatically hand off the content to the KnowledgeSummarizerAgent "
        "for summarization."
    ),
    tools=[web_search],
    tool_use_behavior="stop_on_first_tool",
    handoffs=[summarizer_agent]
)

scheduler_agent = Agent(
    name="StudyPlanSchedulerAgent",
    instructions=(
        "You are a Study Plan Scheduler Agent. Do not ask any questions or request input from the user. "
        "Assume that study topics, deadlines, and available study hours per day are already available in the current context. "
        "Use this information to create a personalized and efficient study plan that:\n"
        "- Evenly distributes study time\n"
        "- Prioritizes topics with earlier deadlines\n"
        "- Includes short breaks\n\n"
        "After creating the study plan, automatically hand off the study topics to the TopicResearchAgent "
        "to gather additional learning resources. If needed, you can use the Research Agent to look up any information "
        "you don't already have."
    ),
    handoffs=[research_agent]
)