from enum import Enum
import re
from subprocess import Popen, PIPE, STDOUT
import threading
import time


class ServerThread(threading.Thread):

    def __init__(self, start_command, working_directory):
        # make sure to invoke the base class constructor before doing anything else to the thread.
        super(ServerThread, self).__init__()

        self.start_command = start_command
        self.working_directory = working_directory
        self.server_process = None

    def run(self):
        self.server_process = Popen(
            self.start_command,
            cwd=self.working_directory,
            stdout=PIPE,
            stdin=PIPE,
            stderr=STDOUT
        )

    def is_running(self):
        # if start() hasn't been called yet, the server_process will be None
        if not self.server_process:
            return False

        # get the the return code of the completed process
        # - a None value indicates that the process hasn't terminated yet
        # - a negative value, -N,  indicates that the process was terminated by signal N
        return_code = self.server_process.poll()

        # the server is running if the return code is None
        return True if return_code is None else False

    def send_raw_command(self, command):
        self.server_process.stdin.write("{}\n".format(command))

    def find_in_stdout(self, expression_map):
        searching = True
        return_value = None

        while searching:
            line = self.server_process.stdout.readline()

            if not line or line == '':
                # we're at EOF and never found what we were looking for so update our last position and return None
                searching = False
                continue

            for regular_expression, value_if_matched in expression_map.iteritems():
                match_result = re.match(regular_expression, line)
                if match_result:
                    searching = False
                    return_value = value_if_matched
                    break

        return return_value


class GameMode(Enum):
    Survival = 0
    Creative = 1
    Adventure = 2
    Spectator = 3


class MinecraftCommandError(Exception):
    pass


class MinecraftServer(object):

    LOG_ENTRY_REGULAR_EXPRESSION = "\[\d{1,2}:\d{1,2}:\d{1,2}] \[Server thread/INFO\]: "

    def __init__(self, config):
        self.config = config
        self.server_thread = ServerThread(config['start_command'], config['working_directory'])

    def start(self):
        if self.is_running():
            raise MinecraftCommandError('Cannot start minecraft server because it is already running.')
        self.server_thread.start()

    def is_running(self):
        return self.server_thread.is_running()

    def stop(self):
        """
        Stops the minecraft server if it is running
        :return: True if the server is now stopped, otherwise False
        """
        if self.is_running():
            self.server_thread.send_raw_command("stop")

        self.server_thread.join(timeout=5)
        return not self.server_thread.isAlive()

    def teleport_player_to_player(self, player_to_teleport, target_player):
        if not self.player_is_logged_on(player_to_teleport):
            raise MinecraftCommandError('player "{}" is not logged on or not found'.format(player_to_teleport))

        if not self.player_is_logged_on(target_player):
            raise MinecraftCommandError('player "{}" is not logged on or not found'.format(target_player))

        self.server_thread.send_raw_command("teleport {} to {}".format(player_to_teleport, target_player))

    def turn_to_day(self):
        self.server_thread.send_raw_command("time set 0")

    def turn_to_night(self):
        self.server_thread.send_raw_command("time set 13000")

    def set_player_gamemode(self, player, gamemode):
        if not isinstance(gamemode, GameMode):
            raise ValueError('gamemode must be of type GameMode(Enum)')

        if not self.player_is_logged_on(player):
            raise MinecraftCommandError('player "{}" is not logged on'.format(player))

        self.server_thread.send_raw_command("gamemode {} {}".format(gamemode.value, player))

    def player_is_logged_on(self, player):
        self.server_thread.send_raw_command("testfor {}".format(player))
        time.sleep(2)
        return self.server_thread.find_in_stdout({
            self.LOG_ENTRY_REGULAR_EXPRESSION + "Found {}".format(player): True,
            self.LOG_ENTRY_REGULAR_EXPRESSION + "Entity '{}' cannot be found".format(player): False
        })
