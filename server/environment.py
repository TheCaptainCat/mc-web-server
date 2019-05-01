import os

from server import app


class Environment:
    def __init__(self):
        self.env = {}

    def __getitem__(self, key):
        item = self.env.get(key, None)
        if item is None:
            item = os.environ.get(key, None)
        return item

    def __setitem__(self, key, value):
        self.env[key] = value

    def get(self, key, default=None):
        item = self[key]
        return item if item is not None else default


environment = Environment()

try:
    with app.open_instance_resource('.env') as f:
        for line in f:
            line = line.decode('utf-8').replace(os.linesep, '')
            args = line.split('=')
            if len(args) != 2 or args[1] == "":
                continue
            var = os.environ.get(args[0], None)
            if var is None:
                var = args[1]
            environment[args[0]] = var
except FileNotFoundError:
    print('** WARNING: No .env file found')


app.config['ENV'] = environment.get('ENV', 'development')
debug = environment.get('DEBUG')
app.config['DEBUG'] = app.config['ENV'] == 'development' if debug is None else debug == 'True'
app.secret_key = environment['SECRET_KEY']

environment['path'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
