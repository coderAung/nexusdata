from nexusdata.orms.services import AsyncNexusService
from test_project.models.post import Post
from test_project.repos.post_repo import PostRepo


class PostService(AsyncNexusService):

    repo:PostRepo

    async def get_all(self) -> list[Post]:
        return await self.repo.get_all()