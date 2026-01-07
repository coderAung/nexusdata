import dataclasses
from enum import Enum

from nexusdata.security.specials import NexusSecurity


@dataclasses.dataclass
class Person:
    id:int
    name:str

    class Role(Enum):
        Admin = "Admin"
        Member = "Member"

    role:Role

current_person:Person = Person(1, "aung aung", Person.Role.Admin)

sec = NexusSecurity(
    user_cls=Person,
    user_supplier=lambda : current_person,
    role_cls=Person.Role,
    role_func=lambda u: u.role,
)

def authorize():
    print("\n++++++++++++++++++")
    print("Method runs.")
    print("++++++++++++++++++")

def test_hello():
    fn = sec.authenticated(authorized_roles=[Person.Role.Member, Person.Role.Admin])(authorize)
    fn()