from flask import Flask
from logging.config import dictConfig
from app.minecraft import MinecraftServer

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')


minecraft_server = MinecraftServer(app.config['MINECRAFT_CONFIGURATION'])
minecraft_server.start()

# routes all need the flask app decorator, so import it
with app.app_context():
    import app.routes
