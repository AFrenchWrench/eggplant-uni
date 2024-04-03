import graphene
import users.schema
import university_requests.schema
import university.schema


class Query(users.schema.Query, university_requests.schema.Query,
            university.schema.Query, graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation, university_requests.schema.Mutation,
               university.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
