# import sqlalchemy

# sql_query = sqlalchemy.text("SELECT * FROM user")
# result = connection.execute

from models import User

users = User.query.all()

for user in users:
    print user.name


