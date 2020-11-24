from SchedulingVisualizer import SchedulingVisualizer
from TaskModel import SporadicTask

def main():
    visualizer = SchedulingVisualizer("non_preemptive_DM", miss_width=0.3)
    # visualizer = SchedulingVisualizer("preemptive_DM", miss_width=0.3, duration=100)
    visualizer.add_task(SporadicTask(25, 5, 22, task_id=0, label="A1"))
    visualizer.add_task(SporadicTask(25, 3, 25, task_id=1, label="A2")) # 8 => 32

    visualizer.add_task(SporadicTask(25, 7, 22, task_id=10, label="B1"))
    visualizer.add_task(SporadicTask(25, 3, 25, task_id=11, label= "B2")) # 10 => 40

    # visualizer.add_task(SporadicTask(100, 20, 92, task_id=20, label="C1"))
    # visualizer.add_task(SporadicTask(100, 8, 100, task_id=21, label="C3")) # 36

    # visualizer.add_task(SporadicTask(100, 11, 81, task_id=20, label="C1"))
    # visualizer.add_task(SporadicTask(100, 11, 92, task_id=21, label="C2"))
    # visualizer.add_task(SporadicTask(100, 8, 100, task_id=22, label="C3"))

    visualizer.add_task(SporadicTask(100, 7.2, 74.1, task_id=20, label="C1"))
    visualizer.add_task(SporadicTask(100, 7.2, 81.3, task_id=21, label="C2"))
    visualizer.add_task(SporadicTask(100, 7.2, 88.5, task_id=21, label="C2"))
    visualizer.add_task(SporadicTask(100, 4.3, 95.7, task_id=22, label="C3"))
    visualizer.add_task(SporadicTask(100, 4.3, 100, task_id=22, label="C3"))




    visualizer.visualization()

if __name__ == "__main__":
    main()
