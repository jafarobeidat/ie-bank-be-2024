from flask_migrate import Migrate
from iebank_api import app, db

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)