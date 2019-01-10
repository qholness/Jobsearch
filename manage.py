from TheHunt import create_app
from TheHunt.db import db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)


manager.add_command('db', MigrateCommand)

def main():
    manager.run()

if __name__ == '__main__':
    main()
