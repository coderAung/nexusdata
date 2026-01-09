from nexusdata.asyncs.decorators import query
from nexusdata.orms.repositories import AsyncNexusRepository
from test_project.models.comment import Comment


class CommentRepo(AsyncNexusRepository[Comment, int]):

    @query(sql="select * from comment")
    async def get_all() -> list[Comment]:pass