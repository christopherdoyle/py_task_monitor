# Task Monitor v0.0.1

## Design
* Run a single instance of server
* Task clients connect to server and declare a task has started. Once their
  task has ended they declare task has ended.
* Query clients connect to server and ask about a task. Server returns 0 for
  not running, 1 for running.
* Task names are limited to around 1000 bytes and must be unique.


## Usage

	>>> taskmonitor.Server('0.0.0.0', 5000).listen()

	>>> taskmonitor.Task('sleep', 'sleep 10', ('0.0.0.0', 5000))

	>>> taskmonitor.query_task('sleep', ('0.0.0.0', 5000))
	1


## Issues

Many issues, this is barely actually code.
