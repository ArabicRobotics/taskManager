import time
import threading
import colorama
from enum import Enum

class TaskStatus(Enum):
	PENDING = 1
	RUNNING = 2
	COMPLETED = 3
	FAILED = 4
	PAUSED = 5
	KILLED = 6


class MessageType:
	INFO = "I"
	DEBUG = "D"
	ERROR = "E"
	VALUE = "V"
	UNKNOWN = "UN"

def stylish_print(message_type, title):
	"""
	Prints a stylish message with a title and message type.

	Args:
		message_type (str): The type of the message (INFO, DEBUG, ERROR, VALUE, UNKNOWN).
		title (str): The title of the message.
	"""
	title_color = colorama.Fore.WHITE

	if message_type == MessageType.INFO:
		title_color = colorama.Fore.CYAN
	elif message_type == MessageType.DEBUG:
		title_color = colorama.Fore.WHITE
	elif message_type == MessageType.ERROR:
		title_color = colorama.Fore.RED
	elif message_type == MessageType.VALUE:
		title_color = colorama.Fore.GREEN

	print(f"{title_color}[{message_type}]{colorama.Style.RESET_ALL}" +" " + f" {title}")

class Task:
	def __init__(self, id=None, name=None, description=None):
		"""
		Initializes a new instance of the class.

		This method initializes the `id`, `name`, `description`, `paused`, `kill`, and `status` attributes of the instance.

Parameters:
			id (int): The unique identifier for the task.
			name (str): The name of the task.
			description (str): The description of the task.

			Returns:
			None
			"""
		self.id = id
		self.name = name
		self.description = description
		self.status = TaskStatus.PENDING
		self.current_step = 0
		self.total_steps = 100

	def run(self):
		thread = threading.Thread(target=self._run)
		thread.start()

	def _run(self) -> None:
		"""
		Runs the task until it is killed or completed.

		Returns:
			None
		"""
		self.status = TaskStatus.RUNNING
		while self.status != TaskStatus.KILLED:
			if self.status == TaskStatus.RUNNING:
				time.sleep(0.5)
				self.current_step += 1
				percentage: float = (self.current_step / self.total_steps) * 100
				self.report_progress(percentage)
				if self.current_step >= self.total_steps:
					self.status = TaskStatus.COMPLETED
					return

	def report_progress(self, percentage):
		stylish_print(MessageType.VALUE, f"Task {self.id}: Progress - {percentage}%")
	def pause(self):
		self.status = TaskStatus.PAUSED

	def resume(self):
		self.status = TaskStatus.RUNNING

	def stop(self):
		self.status = TaskStatus.KILLED

class TaskCollection:
	def __init__(self):
		self.tasks = []

	def add_task(self, task):
		self.tasks.append(task)

	def remove_task(self, task):
		self.tasks.remove(task)
	def manage_tasks(self):
		for task in self.tasks:
			thread = threading.Thread(target=task.run)
			thread.start()
	def report_tasks(self):
		for task in self.tasks:
			print(f"Task {task.id}: Status - {task.status.name}")
# Usage
task1 = Task()
task2 = Task()
task_collection = TaskCollection()
task_collection.add_task(task1)
task_collection.add_task(task2)

task1.run()
# To pause a task
task1.pause()

# To resume a task
task1.resume()
time.sleep(3)
# To stop a task
#task1.stop()
task_collection.report_tasks()
# To manage all tasks in the collection
#task_collection.manage_tasks()


