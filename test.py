from SchedulingVisualizer import SchedulingVisualizer
from TaskModel import SporadicTask

def main():
    print("start")
    visualizer = SchedulingVisualizer("non_preemptive_DM")
    visualizer.add_task(SporadicTask(10, 0.5, 10, task_id=0, label="t1_1"))
    visualizer.add_task(SporadicTask(10, 1, 9.5, task_id=1, label="t1_2"))
    visualizer.add_task(SporadicTask(10, 2, 8.5, task_id=2, label="t1_3"))
    visualizer.add_task(SporadicTask(15, 1, 15, task_id=3, label="t2_1"))
    visualizer.add_task(SporadicTask(15, 3, 14, task_id=4, label="t2_2"))
    visualizer.add_task(SporadicTask(15, 3, 11, task_id=5, label="t2_3"))
    visualizer.add_task(SporadicTask(15, 3, 8, task_id=6, label="t2_4"))

    # visualizer.add_task(SporadicTask(5, 2, 4, task_id=0, label="t1_1"))
    # visualizer.add_task(SporadicTask(3, 2, 2, task_id=1, label="t1_2"))

    visualizer.visualization()



if __name__ == "__main__":
    main()