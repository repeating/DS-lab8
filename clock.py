from multiprocessing import Process, Pipe
from datetime import datetime


def local_time(vector):
    return ' (LAMPORT_TIME={}, LOCAL_TIME={})'.format(vector,
                                                     datetime.now())

def calc_recv_timestamp(recv_time_stamp, vector):
    for id  in range(len(vector)):
        vector[id] = max(recv_time_stamp[id], vector[id])
    return vector

def event(pid, vector):
    vector[pid] +=1
    print('Something happened in {} !'.\
          format(pid) + local_time(vector))
    return vector

def send_message(pipe, pid, vector):
    vector[pid] +=1
    pipe.send(('Empty shell', vector))
    print('Message sent from ' + str(pid) + local_time(vector))
    return vector

def recv_message(pipe, pid, vector):
    message, timestamp = pipe.recv()
    vector[pid] += 1
    vector = calc_recv_timestamp(timestamp, vector)
    print('Message received at ' + str(pid)  + local_time(vector))
    return vector

def process_one(pipe12):
    pid = 0
    vector = [0, 0, 0]
    vector = send_message(pipe12, pid, vector)
    vector = send_message(pipe12, pid, vector)
    vector = event(pid, vector)
    vector = recv_message(pipe12, pid, vector)
    vector = event(pid, vector)
    vector = event(pid, vector)
    vector = recv_message(pipe12, pid, vector)


def process_two(pipe21, pipe23):
    pid = 1
    vector = [0, 0, 0]
    vector = recv_message(pipe21, pid, vector)
    vector = recv_message(pipe21, pid, vector)
    vector = send_message(pipe21, pid, vector)
    vector = recv_message(pipe23, pid, vector)
    vector = event(pid, vector)
    vector = send_message(pipe21, pid, vector)
    vector = send_message(pipe23, pid, vector)
    vector = send_message(pipe23, pid, vector)


def process_three(pipe32):
    pid = 2
    vector = [0, 0, 0]
    vector = send_message(pipe32, pid, vector)
    vector = recv_message(pipe32, pid, vector)
    vector = event(pid, vector)
    vector = recv_message(pipe32, pid, vector)


if name == 'main':
    oneandtwo, twoandone = Pipe()
    twoandthree, threeandtwo = Pipe()

    process1 = Process(target=process_one,
                       args=(oneandtwo,))
    process2 = Process(target=process_two,
                       args=(twoandone, twoandthree))
    process3 = Process(target=process_three,
                       args=(threeandtwo,))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()
