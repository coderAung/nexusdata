# NexusRepo

**NexusData** is a Python data access library that provides a **Spring Data JPA–inspired repository pattern** on top of SQLAlchemy, with first-class compatibility for **SQLModel**.

It enables developers to define repositories using **declarative method names**, **custom queries**, and **DTO projections**, while keeping full access to SQLAlchemy’s power.

### ✨ Key Features
- **Repository Abstraction** inspired by **Spring Data JPA**
- **SQL Alchemy core & ORM support**
- **SQLModel compactible**
- **Method-name–based query generation**
- **DTO / Projection queries**
- **Transaction Management**

### Installation
```commandline
pip install nexusrepo
```

### Demonstration

Let's create a simple crud to learn how to use NexusRepo 

### Creating Models

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class Category(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(nullable=False)


class Product(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(nullable=False)
    price: float = Field(nullable=False)
    category_id: int = Field(foreign_key="category.id")
    category: Category = Relationship()
```

### Creating Repository for each model

```python
from nexusdata.orms.repositories import NexusRepository

class CategoryRepo(NexusRepository[Category, int]):
    pass

class ProductRepo(NexusRepository[Product, int]):
    pass
```

### Using Repository

**NexusRepository** takes **Session** as constructor argument

```python
from sqlmodel import Session, create_engine

engine = create_engine("sqlite:///:memory:")
def get_session():
    with Session(engine) as session:
        yield session
session = next(get_session())        

category_repo = CategoryRepo(session)
product_repo = ProductRepo(session)

```

#### After initializing repositories, we can just use following methods instantly

```commandline
save(entity:MODEL) -> MODEL
save_all(entities:list[MODEL]) -> list[MODEL]
find_by_id(id:ID) -> MODEL
count() -> int
delete(entity:MODEL)
delete_by_id(id:ID)
```

### Query Function

**NexusRepo** supports Spring inspired query method which we can define and use methods without implementing just by following the naming rule.

_for example_

Let's write a function that find products by name and price range.
All you have to do is to add a @query decorator on the function.

```python
from nexusdata.orms.repositories import NexusRepository
from nexusdata.legacy.decorators import query

class ProductRepo(NexusRepository[Product, int]):
    
    @query
    def find_by_name_like_and_price_lte(self, name:str, price:float) -> list[Product]:pass

```

### Query Projection

**NexusRepo** also supports sql projection too. Never return the whole entity, wrap it in a DTO.
To do this, we can use @query decorator again but with sql attribute, user can also pass dto_cls and map_func which accept sqlalchemy's RowMapping and convert to DTO,
for better control.
**_important !_**
Projection columns should reflect the DTO class's constructor argument

_for example_ let's write a function that retrieve category with their product counts

```python
from dataclasses import dataclass
from nexusdata.orms.repositories import NexusRepository
from nexusdata.legacy.decorators import query

@dataclass
class CategoryDto:
    id:int
    name:str
    products:int

    
class CategoryRepo(NexusRepository[Category, int]):
    
    @query(sql="""
        select c.id as id, c.name as name, count(p.id) as products
        from category as c
        left join product as p on p.category_id = c.id
        group by c.id, c.name
    """, dto=CategoryDto)
    def get_all_category_dtos(self) -> list[CategoryDto]:pass

```

### Service

In above example, we introduce **NexusService**, which is also an element of **NexusRepo**, that take Session as constructor argument.
_Point of NexusSession_ is initializing every repositories inside the service automatically.
Therefore, we don't need to create instances for repositories we used in a service.
NexusService does it all for you.


### Transaction

**NexusRepo** also support _@transactional_ decorator for transaction management.
Remember! In **NexusRepo** repositories never commit, therefore, you need to add @transactional decorator on methods to persit.
Recommended - Do it in service layer

_for example_

```python
from nexusdata.orms.services import NexusService
from nexusdata.legacy.decorators import transactional

class ProductForm:
    name:str
    price:float

class ProductService(NexusService):
    repo:ProductRepo

    @transactional
    def save(self, form:ProductForm) -> int:
        p:Product = self.save(Product(name=form.name, price=form.price))
        return p.id

    
    @transactional(read_only=True)
    def get_all(self) -> list[CategoryDto]:
        return self.repo.get_all_category_dtos()
```