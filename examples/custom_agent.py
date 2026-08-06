"""
Example: Custom Agent
=====================

This example shows how to create a custom agent using the Enal AI OS SDK.
"""

import asyncio

from sdk.enal_ai import Agent, EnalAI

# Initialize SDK
enal = EnalAI(api_url="http://localhost:8000")


# Define a custom agent
class MikrotikAgent(Agent):
    name = "mikrotik"
    description = "Mikrotik network configuration agent"
    capabilities = ["networking", "mikrotik", "firewall", "hotspot"]
    model = "gpt-4o"
    temperature = 0.3

    async def execute(self, task: str, context: dict | None = None) -> str:
        # Your custom logic here
        return f"Configured Mikrotik: {task}"


# Register and use
async def main():
    agent = MikrotikAgent()
    result = await agent.run("Configure hotspot with 3 VLANs")
    print(f"Agent: {result['agent']}")
    print(f"Success: {result['success']}")
    print(f"Result: {result['result']}")


if __name__ == "__main__":
    asyncio.run(main())
