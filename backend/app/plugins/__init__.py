import logging
from backend.app.core.mcp_registry import MCPPlugin, MCPTool, MCPResource, MCPResourceType, mcp_registry

logger = logging.getLogger(__name__)


DOCKER_PLUGIN = MCPPlugin(
    id="docker",
    name="Docker",
    version="1.0.0",
    description="Container management and deployment",
    tools=[
        MCPTool(
            name="docker_build",
            description="Build a Docker image",
            input_schema={
                "type": "object",
                "properties": {
                    "dockerfile_path": {"type": "string", "description": "Path to Dockerfile"},
                    "image_name": {"type": "string", "description": "Name for the image"},
                    "context": {"type": "string", "description": "Build context directory"},
                },
                "required": ["dockerfile_path", "image_name"],
            },
            permissions=["execute", "deploy"],
            sandbox=True,
        ),
        MCPTool(
            name="docker_run",
            description="Run a Docker container",
            input_schema={
                "type": "object",
                "properties": {
                    "image_name": {"type": "string", "description": "Image to run"},
                    "ports": {"type": "object", "description": "Port mappings"},
                    "environment": {"type": "object", "description": "Environment variables"},
                },
                "required": ["image_name"],
            },
            permissions=["execute", "deploy"],
            sandbox=True,
        ),
        MCPTool(
            name="docker_ps",
            description="List running containers",
            input_schema={
                "type": "object",
                "properties": {"all": {"type": "boolean", "description": "Show all containers"}},
            },
            permissions=["read"],
            sandbox=False,
        ),
    ],
    resources=[
        MCPResource(
            uri="docker://images",
            name="Docker Images",
            description="List of available Docker images",
            resource_type=MCPResourceType.SERVICE,
            permissions=["read"],
        ),
    ],
)


GITHUB_PLUGIN = MCPPlugin(
    id="github",
    name="GitHub",
    version="1.0.0",
    description="GitHub repository management",
    tools=[
        MCPTool(
            name="github_create_repo",
            description="Create a new GitHub repository",
            input_schema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Repository name"},
                    "description": {"type": "string", "description": "Repository description"},
                    "private": {"type": "boolean", "description": "Private repository"},
                },
                "required": ["name"],
            },
            permissions=["write", "deploy"],
            sandbox=False,
        ),
        MCPTool(
            name="github_push_file",
            description="Push a file to GitHub repository",
            input_schema={
                "type": "object",
                "properties": {
                    "repo": {"type": "string", "description": "Repository name"},
                    "path": {"type": "string", "description": "File path"},
                    "content": {"type": "string", "description": "File content"},
                    "message": {"type": "string", "description": "Commit message"},
                },
                "required": ["repo", "path", "content"],
            },
            permissions=["write", "deploy"],
            sandbox=False,
        ),
    ],
    resources=[
        MCPResource(
            uri="github://repos",
            name="GitHub Repositories",
            description="Access to GitHub repositories",
            resource_type=MCPResourceType.SERVICE,
            permissions=["read"],
        ),
    ],
)


FILESYSTEM_PLUGIN = MCPPlugin(
    id="filesystem",
    name="Filesystem",
    version="1.0.0",
    description="File system operations within workspace",
    tools=[
        MCPTool(
            name="fs_read",
            description="Read a file from workspace",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                },
                "required": ["path"],
            },
            permissions=["read"],
            sandbox=True,
        ),
        MCPTool(
            name="fs_write",
            description="Write a file to workspace",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "content": {"type": "string", "description": "File content"},
                },
                "required": ["path", "content"],
            },
            permissions=["write"],
            sandbox=True,
        ),
        MCPTool(
            name="fs_list",
            description="List files in directory",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path"},
                },
                "required": ["path"],
            },
            permissions=["read"],
            sandbox=True,
        ),
    ],
)


POSTGRES_PLUGIN = MCPPlugin(
    id="postgres",
    name="PostgreSQL",
    version="1.0.0",
    description="PostgreSQL database operations",
    tools=[
        MCPTool(
            name="pg_query",
            description="Execute a SQL query",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "SQL query"},
                    "database": {"type": "string", "description": "Database name"},
                },
                "required": ["query"],
            },
            permissions=["read", "write", "execute"],
            sandbox=True,
        ),
        MCPTool(
            name="pg_migrate",
            description="Run database migrations",
            input_schema={
                "type": "object",
                "properties": {
                    "migrations_path": {"type": "string", "description": "Path to migrations"},
                },
                "required": ["migrations_path"],
            },
            permissions=["write", "execute", "deploy"],
            sandbox=True,
        ),
    ],
    resources=[
        MCPResource(
            uri="postgres://schemas",
            name="Database Schemas",
            description="Database schema information",
            resource_type=MCPResourceType.DATABASE,
            permissions=["read"],
        ),
    ],
)


def register_default_plugins():
    for plugin in [DOCKER_PLUGIN, GITHUB_PLUGIN, FILESYSTEM_PLUGIN, POSTGRES_PLUGIN]:
        mcp_registry.register_plugin(plugin)
    logger.info(f"Registered {len([DOCKER_PLUGIN, GITHUB_PLUGIN, FILESYSTEM_PLUGIN, POSTGRES_PLUGIN])} default MCP plugins")
