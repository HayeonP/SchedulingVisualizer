from numpy.random import seed
from numpy.random import rand

class SporadicTask:
    def __init__(self, min_arrival_time, execution_time, relative_deadline, task_id, label, jitter=0):
        self.min_arrival_time = min_arrival_time
        self.execution_time = execution_time
        self.relative_deadline = relative_deadline
        self.task_id = task_id
        self.label = label
        seed(task_id)
        color = rand(3)
        self.color = (color[0], color[1], color[2])
        self.jitter = jitter

class Job:
    def __init__(self, arrival_time, execution_time, deadline, task_id, label, color):
        self.arrival_time = arrival_time
        self.execution_time = execution_time
        self.deadline = deadline
        self.task_id = task_id
        self.label = label
        self.finish = False
        self.color = color
        self.miss = False

class Unit:
    def __init__(self, start, end, task_id, label, color):
        self.start = start
        self.end = end
        self.task_id = task_id
        self.label = label
        self.color = color

