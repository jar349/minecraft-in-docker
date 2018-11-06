from subprocess import Popen
from flask import current_app
from app import minecraft_server


@current_app.route('/teleport', methods=['POST'])
def teleport(request):

    if not request:
        return 'Bad Request: No data received', 400

    if 'player_to_be_moved' in request and 'destination_player' in request:
        player_to_be_moved = request['player_to_be_moved']
        destination_player = request['destination_player']

        minecraft_server.teleport_player_to_player(player_to_be_moved, destination_player)

@current_app.route('/start', methods=['GET'])
def start():
    print('Received request to start minecraft')
    minecraft_server.start()

@current_app.route('/stop', methods=['GET'])
def stop():
    print('Received request to stop minecraft')
    minecraft_server.stop()
    # we know we're in a docker container that is running nginx as a proxy for uwsgi and we want everything to stop -
    # not just flask, so call out to nginx and send a stop signal.  uwsgi should die too because die-onterm is true
    Popen(["nginx", "-s", "stop"], start_new_session=true)
    print('The server is stopped')
