import os
import requests
from dotenv import load_dotenv
import asyncio
import logging
from swarmzero import Agent, Swarm
from swarmzero.sdk_context import SDKContext

# Load environment variables
load_dotenv()

config_path = "./swarmzero_config.toml"
sdk_context = SDKContext(config_path=config_path)

o3_agent = Agent(
    name="o3_agent",
    instruction="""You are an advanced AI agent specializing in mathematics and logical reasoning. Solve the given problem step-by-step, explaining each calculation and reasoning process clearly. 
    Break the problem into logical steps, highlight key formulas and principles, and ensure clarity in your approach. If the problem involves reasoning, provide a structured explanation of your thought process, including assumptions, deductions, and conclusions. 
    Present the final answer in the simplest form and, if applicable, include an alternative method or approach.""",
    functions=[],
    config_path=config_path,
    chat_only_mode=True,
)

r1_agent = Agent(
    name="r1_agent",
    instruction="""You are an advanced AI agent specializing in mathematics and logical reasoning. Solve the given problem step-by-step, explaining each calculation and reasoning process clearly. 
    Break the problem into logical steps, highlight key formulas and principles, and ensure clarity in your approach. If the problem involves reasoning, provide a structured explanation of your thought process, including assumptions, deductions, and conclusions. 
    Present the final answer in the simplest form and, if applicable, include an alternative method or approach.""",
    functions=[],
    config_path=config_path,
    chat_only_mode=True,
)

Reasoning_Agents_Swarm = Swarm(
    name="Reasoning_Agents_Swarm",
    description="A swarm of AI Agents that can solve math problems and do high level reasoning.",
    instruction="""Upon receiving a math or reasoning problem from the user, follow these steps in order:
    Execute with r1_agent: Pass the problem to r1_agent to generate a solution.
    Print r1_agent's answer: Display the solution provided by r1_agent.
    Execute with o3_agent: Pass the same problem to o3_agent to generate a separate solution.
    Print o3_agent's answer: Display the solution provided by o3_agent.
    Compare and finalize: Ensure both solutions are clearly presented.
    If an agent encounters an issue, retry the execution with slight modifications to the input. Maintain clear and structured outputs for easy comparison.""",
    agents=[
        o3_agent,
        r1_agent,
    ],
    functions=[],
    sdk_context=sdk_context,
    max_iterations=100,
)

async def main():
    print(
        "\nWelcome to the Reasoning Agents Swarm!\n"
        "This swarm can solve math problems and perform high-level reasoning.\n"
        "Type 'exit' to quit.\n"
    )

    while True:
        prompt = input("\nEnter a math or reasoning problem: \n\n")
        if prompt.lower() == "exit":
            break
        try:
            logging.info(f"Problem received: '{prompt}'")

            # Execute with r1_agent
            print("\nSolving with r1_agent...\n")
            r1_response = await Reasoning_Agents_Swarm.chat(prompt, agent="r1_agent")
            print("\nSolution from r1_agent:\n")
            print(r1_response)

            # Execute with o3_agent
            print("\nSolving with o3_agent...\n")
            o3_response = await Reasoning_Agents_Swarm.chat(prompt, agent="o3_agent")
            print("\nSolution from o3_agent:\n")
            print(o3_response)

        except Exception as e:
            logging.error(f"An error occurred during the reasoning process: {e}")
            print("\nAn error occurred while solving the problem. Please try again.\n")


if __name__ == "__main__":
    asyncio.run(main())
