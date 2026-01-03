from tests.conftest import engine
from tests.domain.abstractions import BaseModel
from tests.domain.models import Account
from tests.domain.repos import AccountRepo


def init_db():
    BaseModel.metadata.create_all(engine)


def test_account_repo(account_repo:AccountRepo):
    init_db()
    a1 = Account(name="Aung Aung", email="aung@gmail.com", password="aungaung")
    a2 = Account(name="Su Su", email="su@gmail.com", password="susu")
    a3 = Account(name="Aung Gyi", email="aunggyi@gmail.com", password="aungaung")
    account_repo.save_all([a1, a2, a3])

def test_2(account_repo:AccountRepo):
    result = account_repo.get_dtos_by_name("su%")
    print("===========================")
    print(result)