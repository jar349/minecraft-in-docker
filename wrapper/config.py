import os

# Flask Debugging mode
DEBUG = os.environ.get('FLASK_DEBUG', False)

# Google oauth settings
GOOGLE_CLIENT_ID = os.environ.get('FLASK_GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('FLASK_GOOGLE_CLIENT_SECRET')

# A secret key that will be used for securely signing the session cookie
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', os.urandom(16))

# Get Java memory options from environment variables
JAVA_XMS = os.environ.get('JAVA_XMS', '1024M')
JAVA_XMX = os.environ.get('JAVA_XMX', '1024M')

MINECRAFT_CONFIGURATION = {
    'start_command': [
        '/usr/bin/java',
        '-Xmx' + JAVA_XMX,
        '-Xms' + JAVA_XMS,
        '-jar',
        '/usr/local/minecraft/server.jar',
        'nogui'
    ],
    'working_directory': '/usr/local/minecraft'
}
