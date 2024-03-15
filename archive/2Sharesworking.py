import gc
import cotask
import task_share

def task1_fun(shares):
    my_share, my_queue = shares
    counter = 0
    while True:
        my_share.put(counter)
        #my_queue.put(counter)
        counter += 1
        yield 0

def task2_fun(shares):
    the_share, the_queue = shares
    while True:
        print(f"Share1: {the_share.get()} ", end='')
        #while not the_queue.empty():
        #    print(f"{the_queue.get()} ", end='')
        print('')
        yield 0

def task3_fun(shares2):
    my_share2, my_queue2 = shares2
    counter = 0
    while True:
        my_share2.put(counter)
        #my_queue2.put(counter)
        counter += 1
        yield 0

def task4_fun(shares2):
    the_share2, the_queue2 = shares2
    while True:
        print(f"Share2: {the_share2.get()}", end='')
        #while not the_queue2.empty():
        #    print(f"{the_queue2.get()} ", end='')
        print('')
        yield 0

if __name__ == "__main__":
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")

    share0 = task_share.Share('h', thread_protect=False, name="Share 0")
    share1 = task_share.Share('h', thread_protect=False, name="Share 1")
    #q0 = task_share.Queue('L', 16, thread_protect=False, overwrite=False,
    #                      name="Queue 0")
    #q1 = task_share.Queue('L', 16, thread_protect=False, overwrite=False,
    #                      name="Queue 1")
    
    task1 = cotask.Task(task1_fun, name="Task 1", priority=4, period=100,
                        profile=True, trace=False, shares=(share0, share1))
    task2 = cotask.Task(task2_fun, name="Task 2", priority=2, period=100,
                        profile=True, trace=False, shares=(share0, share1))
    task3 = cotask.Task(task3_fun, name="Task 3", priority=1, period=200,
                        profile=True, trace=False, shares=(share1, share0))
    task4 = cotask.Task(task4_fun, name="Task 4", priority=3, period=200,
                        profile=True, trace=False, shares=(share1, share0))

    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    cotask.task_list.append(task3)
    cotask.task_list.append(task4)

    gc.collect()

    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break

    print('\n' + str(cotask.task_list))
    print(task_share.show_all())

