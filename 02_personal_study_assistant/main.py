# these lines for importing from parent folder in child folder
 
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from setup_config import config
from agents_file import scheduler_agent
from agents import Runner
from hooks import ExampleHooks

user_input = input("Please enter your study topics, deadlines, and available study hours per day: ")
# async def main(input:str):
#     print( await Runner.run_sync(research_agent, input, run_config=config,).final_output)

async def main(user_input):
    result = await Runner.run(scheduler_agent, user_input,hooks=hooks, run_config=config)
    print(result.final_output)
    
if __name__ == "__main__":
    import asyncio
    hooks = ExampleHooks()
    asyncio.run(main(user_input))