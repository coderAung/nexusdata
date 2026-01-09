from nexusdata.asyncs.decorators import query
from nexusdata.orms.repositories import AsyncNexusRepository

from test_project.models.post import Post

class PostRepo(AsyncNexusRepository[Post, int]):

    @query(sql="select * from post")
    async def get_all(self) -> list[Post]:pass