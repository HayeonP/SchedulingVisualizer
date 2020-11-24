from TaskModel import SporadicTask
from TaskModel import Job
from TaskModel import Unit
from math import gcd
import matplotlib.pyplot as plt
import copy
import numpy as np

DEBUG = False
WHITE = (1, 1, 1)
RED = (1, 0, 0)

class SchedulingVisualizer:
    def __init__(self, scheduling_algorithm, taskset=[], size=(30, 15), miss_width=0.3, duration=-1):

        self.scheduling_algorithm = scheduling_algorithm
        self.taskset = taskset
        self.hyper_period = -1
        self.size = size
        self.miss_width = miss_width
        self.duration = duration

    def visualization(self):
        if(self.duration == -1):
            self.duration = self.get_hyper_period()
        jobset_list = []
        for task in self.taskset:
            jobset_list.append(self.get_jobset(task, self.duration))

        fig, ax = plt.subplots()
        ax.set_ylim(0,3)
        ax.set_xlabel("Time")
        ax.xaxis.grid()
        fig.set_size_inches(self.size[0], self.size[1])

        if(self.scheduling_algorithm == "preemptive_DM"):
            print("Working")
            scheduling_units = self.preemptive_DM(jobset_list, self.duration)
        elif(self.scheduling_algorithm == "non_preemptive_DM"):
            scheduling_units = self.non_preemptive_DM(jobset_list, self.duration)
        else:
            print("Wrong algorithm name! ( preemptive_DM / non_preemptie_DM )")
            exit()

        miss_units = []
        for unit in scheduling_units:
            print(round(unit.start,3), round(unit.end,3), self.erase_newline(unit.label))

            if("Miss" in unit.label):
                miss_units.append(unit)
                continue
            elif(unit.label == "none"):
                continue
            ax.text(unit.start + (unit.end-unit.start)/2, 1.5, unit.label, ha='center', va='center', fontsize=15)
            barh = ax.broken_barh([(unit.start, unit.end - unit.start)], (1.4, 0.2), color=[unit.color])
            barh.set_edgecolor("black")
            barh.set_linewidth(4)
        for unit in miss_units:
            ax.text(unit.end, 1.8, unit.label, ha='left', va='center', fontsize=20)
            ax.broken_barh([(unit.start, unit.end - unit.start)], (1.2, 0.6),
                           edgecolor="black", color=[unit.color])

        plt.show()

        # for jobset in jobset_list:
        #     self.print_jobset(jobset)

        return

    def preemptive_DM(self, jobset_list, hyper_period, time_quanta=0.01):
        t = 0

        scheduling_units = []
        cur_unit = Unit(-1, -1, -1, "none", color=WHITE)
        prev_unit = Unit(-1, -1, -1, "none", color=WHITE)

        while (True):
            if(DEBUG):
                print("t:",t)
                print("Prev:", prev_unit.start, prev_unit.end, prev_unit.task_id, prev_unit.label)
            if (t > hyper_period+time_quanta):
                break

            arrival_jobs = self.find_arrival_time_smaller_or_equal_to_time(jobset_list, t+time_quanta-0.02)
            if(DEBUG):
                print("arrival_jobs:",len(arrival_jobs))

            if (len(arrival_jobs) == 1):
                cur_job = arrival_jobs[0]
            elif (len(arrival_jobs) > 1):
                cur_job = min(arrival_jobs, key=lambda job: job.deadline)
            elif(len(arrival_jobs) == 0):
                cur_job = Job(-1,-1,-1, task_id=-1, label="none", color=WHITE)

            cur_unit.label = cur_job.label
            cur_unit.task_id = cur_job.task_id
            cur_unit.color = cur_job.color

            deadline_jobs = self.find_deadline_equal_to_time(jobset_list, t)
            if (len(deadline_jobs) > 0 and cur_job.miss==False):
                cur_job.miss = True
                miss_label = self.erase_newline(cur_unit.label) + " Miss"
                scheduling_units.append(cur_unit)
                scheduling_units.append(Unit(t, t + self.miss_width,
                                             task_id=-1,
                                             label=miss_label,
                                             color=RED))

            if(cur_unit.label == "none" and prev_unit.label == "none"):
                cur_unit.start = -1
                cur_unit.end = -1
            elif(cur_unit.label == "none" and prev_unit.label != "none"):
                scheduling_units.append(prev_unit)
                cur_unit.start = -1
                cur_unit.end = -1
            elif(cur_unit.label != "none" and prev_unit.label == "none"):
                cur_job.execution_time -= time_quanta
                if (cur_job.execution_time <= 0.001):
                    cur_job.finish = True
                cur_unit.start = t
                cur_unit.end = t+time_quanta
            elif(cur_unit.label == prev_unit.label):
                cur_job.execution_time -= time_quanta
                if (cur_job.execution_time <= 0.001):
                    cur_job.finish = True
                cur_unit.start = prev_unit.start
                cur_unit.end = t+time_quanta
            elif(cur_unit.label != prev_unit.label):
                scheduling_units.append(prev_unit)
                cur_job.execution_time -= time_quanta
                if (cur_job.execution_time <= 0.001):
                    cur_job.finish = True
                cur_unit.start = t
                cur_unit.end = t+time_quanta

            if(DEBUG):
                print("Cur:", cur_unit.start, cur_unit.end, cur_unit.task_id, cur_unit.label)
                print("=============================================")

            prev_unit = copy.copy(cur_unit)
            t += time_quanta

        return scheduling_units

    def non_preemptive_DM(self, jobset_list, duration, time_quanta=0.01):
        t = 0

        scheduling_units = []
        cur_unit = Unit(-1, -1, -1, "none", color=WHITE)
        prev_unit = Unit(-1, -1, -1, "none", color=WHITE)
        is_prev_job_finished = True

        while (True):
            if (DEBUG):
                print("t:", t)
                print("Prev:", prev_unit.start, prev_unit.end, prev_unit.task_id, prev_unit.label)
            if (t > duration+time_quanta):
                break
            if(is_prev_job_finished==True):
                arrival_jobs = self.find_arrival_time_smaller_or_equal_to_time(jobset_list, t + time_quanta - 0.02)
                if (DEBUG):
                    print("arrival_jobs:", len(arrival_jobs))

                if (len(arrival_jobs) == 1):
                    cur_job = arrival_jobs[0]
                elif (len(arrival_jobs) > 1):
                    cur_job = min(arrival_jobs, key=lambda job: job.deadline)
                elif (len(arrival_jobs) == 0):
                    cur_job = Job(-1, -1, -1, task_id=-1, label="none", color=WHITE)

                cur_unit.label = cur_job.label
                cur_unit.task_id = cur_job.task_id
                cur_unit.color = cur_job.color
                if(cur_unit.label=="none"):
                    is_prev_job_finished = True
                else:
                    is_prev_job_finished = False

            deadline_jobs = self.find_deadline_equal_to_time(jobset_list, t)
            if (len(deadline_jobs) > 0 and cur_job.miss==False):
                cur_job.miss = True
                miss_label = self.erase_newline(cur_unit.label) + " Miss"
                scheduling_units.append(cur_unit)
                scheduling_units.append(Unit(t, t + self.miss_width,
                                             task_id=-1,
                                             label=miss_label,
                                             color=RED))


            if (cur_unit.label == "none" and prev_unit.label == "none"):
                cur_unit.start = -1
                cur_unit.end = -1
            elif (cur_unit.label == "none" and prev_unit.label != "none"):
                scheduling_units.append(prev_unit)
                cur_unit.start = -1
                cur_unit.end = -1
            elif (cur_unit.label != "none" and prev_unit.label == "none"):
                cur_job.execution_time -= time_quanta
                if (cur_job.execution_time <= 0.001):
                    cur_job.finish = True
                    is_prev_job_finished = True
                cur_unit.start = t
                cur_unit.end = t + time_quanta
            elif (cur_unit.label == prev_unit.label):
                cur_job.execution_time -= time_quanta
                if (cur_job.execution_time <= 0.001):
                    cur_job.finish = True
                    is_prev_job_finished = True
                cur_unit.start = prev_unit.start
                cur_unit.end = t + time_quanta
            elif (cur_unit.label != prev_unit.label):
                scheduling_units.append(prev_unit)
                cur_job.execution_time -= time_quanta
                if (cur_job.execution_time <= 0.001):
                    cur_job.finish = True
                    is_prev_job_finished = True
                cur_unit.start = t
                cur_unit.end = t + time_quanta

            if (DEBUG):
                print("Cur:", cur_unit.start, cur_unit.end, cur_unit.task_id, cur_unit.label)
                print("=============================================")

            prev_unit = copy.copy(cur_unit)
            t += time_quanta

        return scheduling_units

    def erase_newline(self, text):
        return text.replace("\n","")

    def add_task(self, task):
        self.taskset.append(task)
        return

    def get_hyper_period(self):
        periods = []
        for task in self.taskset:
            periods.append(task.min_arrival_time)
        lcm = periods[0]
        for period in periods[1:]:
            lcm = lcm*period//gcd(lcm,period)
        hyper_period = lcm
        return hyper_period

    def get_jobset(self, task, hyper_period):
        number_of_job = hyper_period//task.min_arrival_time
        jobset = []
        arrival_time = task.jitter
        base_label = task.label
        for n in range(number_of_job):
            jobset.append(
                Job(arrival_time=arrival_time, execution_time=task.execution_time,
                    deadline=arrival_time+task.relative_deadline,
                    task_id=task.task_id, label=base_label+"\n("+str(n+1)+")", color=task.color)
            )
            arrival_time += task.min_arrival_time

        return jobset

    def print_jobset(self, jobset):
        for i in range(len(jobset)):
            print("Job",i,":",jobset[i].arrival_time, "\t", jobset[i].execution_time, "\t", jobset[i].deadline, jobset[i].label)
        return

    def check_deadline_miss(self, job, t):
        if(job.deadline > t):
            return True
        return False

    def find_deadline_equal_to_time(self, jobset_list, time):
        result = []
        for jobset in jobset_list:
            for job in jobset:
                if(job.finish==True):
                    continue
                if(job.deadline >= time-0.05 and job.deadline <= time+0.05):
                    result.append(job)
        return result

    def find_arrival_time_smaller_or_equal_to_time(self, jobset_list, time):
        result = []
        for jobset in jobset_list:
            for job in jobset:
                if (job.finish == True):
                    continue
                if(job.arrival_time <= time):
                    result.append(job)

        return result