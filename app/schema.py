import strawberry
from app.user.graphql.queries import UserQuery
from app.user.graphql.subscriptions import UserSubscription

@strawberry.type
class Query(UserQuery):
    pass

@strawberry.type
class Subscription(UserSubscription):
    pass


schema = strawberry.Schema(query=Query, subscription=Subscription)
