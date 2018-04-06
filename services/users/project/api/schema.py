# import graphene
# from graphene import relay
# from graphene_sqlalchemy import SQLAlchemyObjectType,\
# SQLAlchemyConnectionField
# from project.api.models import User as UserModel,\
#     Req as ReqModel,\
#     Lesson as LessonModel,\
#     School as SchoolModel,\
#     Room as RoomModel,\
#     Classgroup as ClassgroupModel
#
#
# class Req(SQLAlchemyObjectType):
#     class Meta:
#         model = ReqModel
#         interfaces = (relay.Node, )
#
#
# class User(SQLAlchemyObjectType):
#     class Meta:
#         model = UserModel
#         interfaces = (relay.Node, )
#
#
# class Lesson(SQLAlchemyObjectType):
#     class Meta:
#         model = LessonModel
#         interfaces = (relay.Node, )
#
#
# class School(SQLAlchemyObjectType):
#     class Meta:
#         model = SchoolModel
#         interfaces = (relay.Node, )
#
#
# class Room(SQLAlchemyObjectType):
#     class Meta:
#         model = RoomModel
#         interfaces = (relay.Node, )
#
#
# class Classgroup(SQLAlchemyObjectType):
#     class Meta:
#         model = ClassgroupModel
#         interfaces = (relay.Node, )
#
#
# class Query(graphene.ObjectType):
#     node = relay.Node.Field()
#     all_users = SQLAlchemyConnectionField(User)
#     all_reqs = SQLAlchemyConnectionField(Req)
#     all_rooms = SQLAlchemyConnectionField(Room)
#
#     def user_reqs(self, user_id):
#         query = Req.query.filter_by(user_id=user_id)
#         return query.all()
#
#
# schema = graphene.Schema(query=Query)
