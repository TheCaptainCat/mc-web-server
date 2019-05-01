import os


if __name__ == '__main__':
    from server import app, socketio
    socketio.run(app)
