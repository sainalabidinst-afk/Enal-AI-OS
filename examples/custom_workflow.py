"""
Example: Custom Workflow
========================

This example shows how to create a custom workflow using the Enal AI OS SDK.
"""

import asyncio
from sdk import Workflow, WorkflowStep, EnalAI

enal = EnalAI()


class ERPBuildWorkflow(Workflow):
    name = "erp-build"
    description = "Build a complete ERP system"

    def __init__(self):
        super().__init__(
            name=self.name,
            description=self.description,
            steps=[
                WorkflowStep(id="1", name="Analyze Requirements", agent="analyst", action="analyze_requirements"),
                WorkflowStep(id="2", name="Design Architecture", agent="architect", action="design_architecture", depends_on=["1"]),
                WorkflowStep(id="3", name="Build Backend", agent="backend-dev", action="build_backend", depends_on=["2"]),
                WorkflowStep(id="4", name="Build Frontend", agent="frontend-dev", action="build_frontend", depends_on=["2"]),
                WorkflowStep(id="5", name="Setup Database", agent="db-admin", action="setup_database", depends_on=["2"]),
                WorkflowStep(id="6", name="Write Tests", agent="qa", action="write_tests", depends_on=["3", "4", "5"]),
                WorkflowStep(id="7", name="Deploy", agent="devops", action="deploy", depends_on=["6"]),
            ],
        )


async def main():
    workflow = ERPBuildWorkflow()
    result = await workflow.execute({"project_id": "erp-001"})
    print(f"Workflow: {result['workflow']}")
    for step_id, step_result in result["results"].items():
        print(f"Step {step_id}: {step_result['status']}")


if __name__ == "__main__":
    asyncio.run(main())
