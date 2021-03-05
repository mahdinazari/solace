from flask_script import Manager
from flask_migrate import MigrateCommand

from application.app import create_app
from application.extensions import db
from models.member import Member


app = create_app('application.config.Config')
manager = Manager(app)


@manager.command
def create_db():
    """
    Create Database
    """
    db.create_all()


@manager.command
def drop_db():
    """
    Drop Database
    """
    db.drop_all()


@manager.command
def create_member(email, password):
    member = Member(email=email)
    member.hashed_password = member.hash_password(password)
    db.session.add(member)
    db.session.commit()
    print("user Added")


manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

