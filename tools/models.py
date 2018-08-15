from datetime import datetime
from bson import ObjectId


class BaseModel(object):

    id = ObjectId()
    date_created = datetime.now()
    date_modified = None


class User(BaseModel):

    user_id = None
    username = ''
    email = ''
    nickname = ''
    first_name = ''
    last_name = ''
    active = True
    plate_number = ''

    def __repr__(self):
        return '<User {} - {} - {}>'.format(
            self.user_id,
            'Active' if self.active else 'Inactive',
            self.plate_number)


#  class Pair(Base):
#     __tablename__ = 'pairs'

#     first_user_id = Column(
#         Integer, ForeignKey('users.user_id'))
#     first_user = relationship('User', foreign_keys=[first_user_id])

#     second_user_id = Column(
#         Integer, ForeignKey('users.user_id'))
#     second_user = relationship('User', foreign_keys=[second_user_id])

#     count = Column(Integer, default=0)

#     def __repr__(self):
#         return '<Pair {} <-> {} - {}>'.format(
#             self.first_user.id, self.second_user.id, self.count)
