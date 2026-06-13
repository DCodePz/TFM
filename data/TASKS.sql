DROP TABLE IF EXISTS TASKS;

CREATE TABLE IF NOT EXISTS TASKS (
    task_id INTEGER PRIMARY KEY,
    pickup_x INTEGER NOT NULL,
    pickup_y INTEGER NOT NULL,
    dropoff_x INTEGER NOT NULL,
    dropoff_y INTEGER NOT NULL,
    assigned_to INTEGER
);

SELECT count(*) FROM TASKS;