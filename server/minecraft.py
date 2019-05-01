import os
import subprocess
from threading import Thread

from server import env


class ServerThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.process = None
        self.running = False
        self.running_callback = None
        self.stdout_callback = None

    def notify_running(self):
        if self.running_callback is not None:
            self.running_callback(ServerRunner.server_status())

    def run(self):
        self.running = True
        self.notify_running()
        self.process = subprocess.Popen(['java', '-Xmx1024M', '-Xms1024M', '-jar',
                                         os.path.join(env['path'], 'mcserver/server.jar'),
                                         'nogui'],
                                        cwd=os.path.join(env['path'], 'mcserver'),
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE)
        for line in iter(self.process.stdout.readline, ''):
            if len(line) > 0:
                if self.stdout_callback is not None:
                    self.stdout_callback(line.rstrip().decode('utf-8'))
            else:
                break
        self.running = False
        self.notify_running()
        ServerRunner.server = None

    def write(self, command):
        if self.running:
            self.process.stdin.write((command + '\n').encode('UTF-8'))
            self.process.stdin.flush()


class ServerRunner:
    server = None
    running_callback = None
    stdout_callback = None

    @classmethod
    def init_server(cls):
        cls.server = ServerThread()
        cls.server.running_callback = cls.running_callback
        cls.server.stdout_callback = cls.stdout_callback

    @classmethod
    def start(cls):
        if cls.server is None:
            cls.init_server()
        if not cls.server.running:
            cls.server.start()

    @classmethod
    def write(cls, command):
        if cls.server is None:
            cls.init_server()
        cls.server.write(command)

    @classmethod
    def server_status(cls):
        return 'running' if cls.server is not None and cls.server.running else 'stopped'
