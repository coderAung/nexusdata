from nexusdata.orms.repositories import AsyncNexusRepository
from test_project.models.comment import Comment


class CommentRepo(AsyncNexusRepository[Comment, int]):pass