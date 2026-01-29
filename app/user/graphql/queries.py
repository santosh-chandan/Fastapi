import strawberry
from app.user.graphql.types import User
from typing import Optional

@strawberry.type
class UserQuery:

    @strawberry.field
    def get_user(self, info, id: int) -> Optional[User]:
        # user = servic.get_by_id(id)
        return User(
            id = 1,
            name = "Snatohs",
            email = "santosh@gastapi.com"
        )
