import sqlite3
import random

conn = sqlite3.connect(".\\data\\Skynet.sqlite")
cur = conn.cursor()

TOTAL_TASKS = 10000
EVERY_X = 5

def generate_id():
    return random.getrandbits(63)

def generate_task():
    px, py = random.randint(0, 100), random.randint(0, 100)
    dx, dy = random.randint(0, 100), random.randint(0, 100)
    return px, py, dx, dy

batch = []

for i in range(1, TOTAL_TASKS + 1):

    px, py, dx, dy = generate_task()

    # tarea normal
    batch.append((generate_id(), px, py, dx, dy, None))

    # duplicada cada X
    if i % EVERY_X == 0:
        batch.append((generate_id(), px, py, dx, dy, None))

    # inserción por lotes
    if len(batch) >= 1000:
        cur.executemany("""
            INSERT INTO TASKS (task_id, pickup_x, pickup_y, dropoff_x, dropoff_y, assigned_to)
            VALUES (?, ?, ?, ?, ?, ?)
        """, batch)
        batch.clear()

if batch:
    cur.executemany("""
        INSERT INTO TASKS (task_id, pickup_x, pickup_y, dropoff_x, dropoff_y, assigned_to)
        VALUES (?, ?, ?, ?, ?, ?)
    """, batch)

conn.commit()
conn.close()