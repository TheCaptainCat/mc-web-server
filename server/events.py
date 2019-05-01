from server import socketio, ServerRunner


@socketio.on('start')
def handle_server_event():
    ServerRunner.start()


@socketio.on('command')
def handle_command_event(command):
    ServerRunner.write(command)


@socketio.on('server_status')
def handle_server_status_event():
    socketio.emit('server_status', ServerRunner.server_status())


def server_running_callback(status):
    socketio.emit('server_status', status, broadcast=True)


def server_stdout_callback(message):
    socketio.emit('server_message', message, broadcast=True)


ServerRunner.running_callback = server_running_callback
ServerRunner.stdout_callback = server_stdout_callback
