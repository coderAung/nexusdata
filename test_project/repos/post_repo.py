from nexusdata.asyncs.decorators import query
from nexusdata.orms.repositories import AsyncNexusRepository
from test_project.configs.dtos import PostItem

from test_project.models.post import Post

class PostRepo(AsyncNexusRepository[Post, int]):

    @query(sql="select * from post")
    async def get_all(self) -> list[Post]:pass

    @query(sql="""
        select 
            p.id as id, p.content as content, p.created_at as created_at,
            a.name as account_name, count(c.id) as comments
            from post as p
            join account as a on a.id = p.account_id
            left join comment as c on c.post_id = p.id
            group by p.id, p.content, p.created_at, a.name
    """, dto=PostItem)
    async def get_post_items(self) -> list[PostItem]:pass