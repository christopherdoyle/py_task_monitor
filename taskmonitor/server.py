import socket
import sys
import threading

from . import common


running_tasks = set()


class Server(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(
                target=self.listen_to_client,
                args=(client,address)
            ).start()

    def listen_to_client(self, client, address):
        # TODO maybe clean up control flow if poss
        size = common.PACKET_SIZE
        task_name = None
        while True:
            try:
                data = client.recv(size)
                if data:
                    if data == common.HEARTBEAT:
                        response = data
                        client.send(response)
                    elif data.startswith(common.START_TASK_PRE):
                        task_name = data[len(common.START_TASK_PRE):]
                        self.add_task(task_name)
                    elif data.startswith(common.END_TASK_PRE):
                        this_task_name = data[len(common.END_TASK_PRE):]
                        # clients can't end other clients
                        if this_task_name == task_name:
                            self.remove_task(task_name, client)
                    elif data.startswith(common.QUERY_TASK_PRE):
                        query_task_name = data[len(common.QUERY_TASK_PRE):]
                        self.query_task(query_task_name, client)
                    else:
                        print('Unhandled msg: {}'.format(data))
                else:
                    # TODO: is this appropriate here or should we just ignore?
                    break
            except Exception as e:
                # TODO finer handling
                print(e)
                client.close()
                return False

        client.close()
        return True

    def add_task(self, task_name):
        running_tasks.add(task_name)
        print('{} started'.format(task_name))

    def query_task(self, task_name, client):
        if task_name in running_tasks:
            response = b'1'
        else:
            response = b'0'
        client.send(response)

    def remove_task(self, task_name, client):
        running_tasks.remove(task_name)
        print('{} ended'.format(task_name))


if __name__ == '__main__':
    # TODO use argparse
    args = sys.argv[1:]
    if len(args) == 1:
        Server('', int(args[0])).listen()
    else:
        print('python server.py port_number')
