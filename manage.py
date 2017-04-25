import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from chat import app, database


migrate = Migrate(app, database)
manager = Manager(app)

manager.add_command('database', MigrateCommand)


if __name__ == '__main__':
    manager.run()
