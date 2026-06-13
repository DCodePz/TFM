DROP TABLE IF EXISTS WORKERS;

CREATE TABLE IF NOT EXISTS WORKERS (
    operario TEXT PRIMARY KEY,
    pos_x INTEGER NOT NULL,
    pos_y INTEGER NOT NULL
);

INSERT INTO WORKERS (operario, pos_x, pos_y) VALUES
    ('Dani', 0, 0),
    ('Julio', 20, 20);

SELECT * FROM WORKERS;
