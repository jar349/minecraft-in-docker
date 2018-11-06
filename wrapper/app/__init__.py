from flask import Flask
from app.minecraft import MinecraftServer

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')

minecraft_server = MinecraftServer(app.config['MINECRAFT_CONFIGURATION'])

from app import routes
app.register_blueprint(routes.bp)


