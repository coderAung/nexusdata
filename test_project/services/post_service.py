from nexusdata.asyncs.decorators import transactional
from nexusdata.orms.services import AsyncNexusService
from test_project.configs.dtos import PostForm, PostItem, ModificationResult
from test_project.models.post import Post
from test_project.repos.post_repo import PostRepo


class PostService(AsyncNexusService):

    repo:PostRepo

    @transactional(read_only=True)
    async def get_all(self) -> list[PostItem]:
        return await self.repo.get_post_items()

    @transactional(read_only=False)
    async def save(self, form:PostForm, account_id:int) -> ModificationResult[int]:
        post = Post(content=form.content, account_id=account_id)
        post = await self.repo.save(post)
        return ModificationResult(id=post.id)

    @transactional
    async def delete_by_id(self, _id:int):
        await self.repo.delete_by_id(_id)