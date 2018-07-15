import socket
import subprocess
import sys
import threading
import time

from . import common


class ThreadedSubprocess(threading.Thread):

    def __init__(self, command, callback):
        self.command = command
        self.callback = callback
        super(ThreadedSubprocess, self).__init__()

    def run(self):
        self.process = subprocess.Popen(
            self.command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, error = self.process.communicate()
        return_code = self.process.wait()
        self.callback(output, error, return_code)


class Task(object):

    def __init__(self, task_name, command, server_conf):
        self.task_name = task_name
        self.command = command
        self.server_conf = server_conf
        self.ended = False

    def execute(self):
        self.open_server_chat()
        self.process = ThreadedSubprocess(self.command, self.on_task_finish)
        self.process.run()
        self.keep_server_chatting()

    def keep_server_chatting(self):
        while not self.ended:
            time.sleep(30)
            try:
                self.socket.send(common.HEARTBEAT)
            except socket.error:
                self.open_server_chat()

    def on_task_finish(self, output, error, return_code):
        print('Return code: {}'.format(return_code))
        self.ended = True
        self.close_server_chat()

    def open_server_chat(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.server_conf)
        msg = common.get_start_task_msg(self.task_name)
        self.socket.send(msg)

    def close_server_chat(self):
        msg = common.get_end_task_msg(self.task_name)
        self.socket.send(msg)
        self.socket.close()


def main(task_name, command, server_address):
    server_ip, server_port = server_address.split(':')
    server_port = int(server_port)

    task = Task(task_name, command, (server_ip, server_port))
    task.execute()


def print_help(error=None):
    if error:
        print(error)
    print('Help')


if __name__ == '__main__':
    # TODO: use argparse
    args = sys.argv[1:]
    if len(args) != 3:
        print_help(error='Invalid number of arguments')
    else:
        main(args[0], args[1], args[2])
