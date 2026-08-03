from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_restful import Api
from sqlalchemy import MetaData

from config import config_by_name


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})


db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
ma = Marshmallow()



def create_app(config_name='development'):
    app = Flask(__name__)

    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    api = Api(app, prefix='/api')


    @app.get('/')
    def index():
        return jsonify({"message" : "my workout application"}), 200
    
    return app