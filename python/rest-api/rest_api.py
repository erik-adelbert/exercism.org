"""
rest_api.py --
"""

from collections import OrderedDict
from dataclasses import dataclass, field, fields, asdict
from functools import partial, wraps
import json


class BadRequest(Exception):
    """custom bad request"""


def jsonio_handler(func: callable) -> callable:  # pylint: disable=C0116
    @wraps(func)
    def wrapper(self, url, payload=None):
        try:
            if payload:
                try:
                    payload = json.loads(payload)
                except json.JSONDecodeError as exc:
                    raise BadRequest from exc

            return json.dumps(func(self, url, payload))
        except BadRequest:
            return json.dumps({"details": "bad request"})

    return wrapper


def from_dict(klass, d):
    """Create a dataclass instance from a dict"""
    try:
        fieldtypes = {f.name: f.type for f in fields(klass)}
        return klass(**{f: from_dict(fieldtypes[f], d[f]) for f in d})
    except:  # pylint: disable=bare-except
        return d  # Not a dataclass field


@dataclass
class User:
    """User abstraction"""

    name: str = ""
    owes: OrderedDict[str, float] = field(default_factory=OrderedDict)
    owed_by: OrderedDict[str, float] = field(default_factory=OrderedDict)
    balance: float = 0.0


@dataclass(init=False)
class UserDB:
    """A toy in-memory User DB"""

    userdb: list[User] = field(default_factory=list)

    def __init__(self, db) -> None:
        to_user = partial(from_dict, User)
        self.userdb = list(map(to_user, db["users"]))  # batch convert to User instances

    # ToyDB methods
    def get(self, fun: callable) -> list[User]:  # pylint: disable=C0116
        return list(filter(fun, self.userdb))

    def add(self, user: User):  # pylint: disable=C0116
        if user.name not in set(u.name for u in self.userdb):
            self.userdb.append(user)

    def delete(self, user: User):  # pylint: disable=C0116
        user = self.get(lambda x: x.name == user.name)[0]

        updates: list[User] = []

        for u in user.owes.keys():
            # pylint: disable=cell-var-from-loop
            lender = self.get(lambda x: x.name == u)[0]
            del lender.owed_by[user.name]
            updates.append(lender)

        for u in user.owed_by.keys():
            # pylint: disable=cell-var-from-loop
            lendee = self.get(lambda x: x.name == u)[0]
            del lendee.owes[user.name]
            updates.append(lendee)

        self.userdb.remove(user)
        for u in updates:
            self.update(u)

    def update(self, user: User):  # pylint: disable=C0116
        user.owed_by = OrderedDict(
            sorted(user.owed_by.items(), key=lambda x: x[0]),
        )
        user.balance = sum(user.owed_by.values()) - sum(user.owes.values())

        for i, u in enumerate(self.userdb):
            if u.name == user.name:
                self.userdb[i] = user


@dataclass(init=False)
class RestAPI:
    """A toy REST API"""

    # In Memory ToyDB
    db: UserDB

    def __init__(self, db) -> None:
        self.db = UserDB(db)  # batch convert to User instances

    # GET handler
    @jsonio_handler
    def get(self, url, payload: str | None = None) -> str:
        """universal GET handler"""

        # route request
        match url:
            case "/users":
                if payload is None:  # query all users
                    users = self.db.get(lambda _: True)
                else:  # query at least one
                    try:
                        names = payload["users"]
                        users = self.db.get(lambda x: x.name in names)
                    except (KeyError, TypeError) as exc:
                        raise BadRequest from exc

                return {"users": list(map(asdict, users))}

            case _:
                raise BadRequest

    # POST handler
    @jsonio_handler
    def post(self, url: str, payload: str | None = None):
        """universal POST handler"""

        match url:
            case "/add":
                try:
                    name: str = payload["user"]
                    self.db.add((u := User(name)))
                    return asdict(u)
                except (KeyError, TypeError) as exc:
                    raise BadRequest from exc

            case "/delete":
                try:
                    name: str = payload["user"]
                    self.db.delete(User(name))
                    return {"details": f"{name} deleted"}
                except (KeyError, TypeError) as exc:
                    raise BadRequest from exc

            case "/iou":
                # get query args
                try:
                    user1_str, user2_str, val = payload.values()

                    # query user1&2
                    user1 = self.db.get(lambda x: x.name == user1_str)[0]
                    user2 = self.db.get(lambda x: x.name == user2_str)[0]
                except (ValueError, IndexError) as exc:
                    raise BadRequest from exc

                balance = val  # a -> b
                if user2_str in user1.owes:
                    balance -= user1.owes[user2_str]  # a -> b

                # unlink user1&2
                for u1, u2 in (
                    (user1, user2_str),
                    (user2, user1_str),
                ):
                    u1.owes.pop(u2, None)
                    u1.owed_by.pop(u2, None)

                # relink/update user1&2
                if balance < 0:
                    user1.owes[user2_str] = user2.owed_by[user1_str] = -balance
                elif balance > 0:
                    user1.owed_by[user2_str] = user2.owes[user1_str] = balance

                # sort outputs
                users = (user1, user2) if user1.name < user2.name else (user2, user1)

                # commit user1&2
                for u in users:
                    self.db.update(u)

                return OrderedDict({"users": list(map(asdict, users))})

            case _:
                raise BadRequest


# database = {
#     "users": [
#         {"name": "Adam", "owes": {"Bob": 3.0}, "owed_by": {}, "balance": -3.0},
#         {"name": "Bob", "owes": {}, "owed_by": {"Adam": 3.0}, "balance": 3.0},
#     ]
# }
# api = RestAPI(database)
# print(api.post("/add", '{"user": "Alice"}'))
# print(api.post("/iou", '{"user1": "Alice", "user2": "Bob", "amount": 50}'))
# print(api.post("/invalid", "{}"))
# print(api.get("/users"))
# print(api.get("/users", '{"users": ["Alice"]}'))
# print(api.post("/delete", '{"user": "Alice"}'))
# print(api.get("/users"))
