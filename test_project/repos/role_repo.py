from nexusdata.orms.repositories import AsyncNexusRepository

from test_project.models.role import Role

class RoleRepo(AsyncNexusRepository[Role, int]):pass