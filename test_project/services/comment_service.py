from nexusdata.asyncs.decorators import transactional
from nexusdata.orms.services import AsyncNexusService
from test_project.configs.dtos import CommentForm, ModificationResult
from test_project.models.comment import Comment
from test_project.repos.comment_repo import CommentRepo
from test_project.repos.post_repo import PostRepo
from test_project.utils.exception import AppBusinessException


class CommentService(AsyncNexusService):

    comment_repo:CommentRepo
    post_repo:PostRepo

    @transactional(read_only=True)
    async def get_all(self) -> list[Comment]:
        return await self.comment_repo.get_all()

    @transactional
    async def save(self, form:CommentForm, account_id:int) -> ModificationResult[int]:

        post = await self.post_repo.find_by_id(form.post_id)
        if post is None:
            raise AppBusinessException("Post does not exists.")

        comment = await self.comment_repo.save(Comment(content=form.content, post_id=form.post_id, account_id=account_id))
        return ModificationResult(id=comment.id)

    @transactional
    async def delete_by_id(self, _id:int):
        await self.comment_repo.delete_by_id(_id)