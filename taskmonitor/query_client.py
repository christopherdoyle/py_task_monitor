import socket
import sys

from . import common


def main(task_name, server_conf):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(server_conf)
    msg = common.get_query_task_msg(task_name)
    conn.send(msg)

    return_code = None

    while True:
        data = conn.recv(common.PACKET_SIZE)
        if data:
            try:
                return_code = int(data)
                break
            except ValueError:
                print('Unexpected response: {}'.format(data), file=sys.stderr)
                break
        else:
            break

    conn.close()
    return return_code
