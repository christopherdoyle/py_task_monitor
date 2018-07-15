HEARTBEAT = b'TUK TUK'
START_TASK_PRE = b'START:'
END_TASK_PRE = b'END:'
QUERY_TASK_PRE = b'QUERY:'
PACKET_SIZE = 1024

DEFAULT_IP = '0.0.0.0'
DEFAULT_PORT = 5000


def _concat(pre_bytes, s):
    return pre_bytes + bytes(s, 'utf-8')


def get_start_task_msg(task_name):
    return _concat(START_TASK_PRE, task_name)


def get_end_task_msg(task_name):
    return _concat(END_TASK_PRE, task_name)


def get_query_task_msg(task_name):
    return _concat(QUERY_TASK_PRE, task_name)
