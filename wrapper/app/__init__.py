from flask import Flask
from app.minecraft import MinecraftServer


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')


minecraft_server = MinecraftServer(app.config['MINECRAFT_CONFIGURATION'])
minecraft_server.start()

# routes all need the flask app decorator, so import it
with app.app_context():
    import app.routes
