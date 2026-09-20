# database/database.py

import sqlite3

from database.map_point import MapPoint


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(
            "points.db",
            check_same_thread=False
        )

        self.create_table()
        self.create_settings_table()

    def create_table(self):
        self.conn.execute(
            """
        CREATE TABLE IF NOT EXISTS points
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            latitude REAL,

            longitude REAL,

            time TEXT,

            visited INTEGER,

            sequence INTEGER
        )
        """
        )

        self.conn.commit()
        
    def create_settings_table(self):

        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS settings
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                setting_name TEXT NOT NULL UNIQUE,

                value TEXT NOT NULL
            )
            """
        )

        self.conn.commit()

    def get_setting(self, setting_name):

        row = self.conn.execute(
            """
            SELECT value
            FROM settings
            WHERE setting_name=?
            """,
            (
                setting_name,
            )
        ).fetchone()

        if row is None:
            return None

        return row[0]


    def set_setting(self, setting_name, value):

        self.conn.execute(
            """
            INSERT INTO settings
            (
                setting_name,
                value
            )
            VALUES (?, ?)

            ON CONFLICT(setting_name)
            DO UPDATE SET
                value=excluded.value
            """,
            (
                setting_name,
                str(value)
            )
        )

        self.conn.commit()

    def save_points(self, points):
        for p in points:
            if p.id is None:
                cur = self.conn.execute(
                    """
                INSERT INTO points
                (
                    latitude,
                    longitude,
                    time,
                    visited,
                    sequence
                )

                VALUES (?,?,?,?,?)
                """,
                    (
                        p.latitude,
                        p.longitude,
                        p.time,
                        int(p.visited),
                        p.sequence
                    )
                )

                p.id = cur.lastrowid

            else:
                self.conn.execute(
                    """
                UPDATE points SET

                latitude=?,
                longitude=?,
                time=?,
                visited=?,
                sequence=?

                WHERE id=?

                """,
                    (
                        p.latitude,
                        p.longitude,
                        p.time,
                        int(p.visited),
                        p.sequence,
                        p.id
                    )
                )

            p.in_database = True

        self.conn.commit()

    def load_points(self):
        rows = self.conn.execute(
            """
        SELECT
            id,
            latitude,
            longitude,
            time,
            visited,
            sequence

        FROM points
        """
        ).fetchall()

        result = []

        for r in rows:
            p = MapPoint(
                r[1],
                r[2],
                r[0],
                r[3]
            )

            p.visited = bool(r[4])
            p.sequence = r[5]
            p.in_database = True

            result.append(p)

        return result

    def delete_points(self, ids):
        print("database delete point")
        for pid in ids:
            self.conn.execute(
                """
            DELETE FROM points
            WHERE id=?
            """,
                (
                    pid,
                )
            )

        self.conn.commit()
    
    def set_visited(self, point_id, visited):
        
        print("set visited: ", point_id)
        
        self.conn.execute(
            """
        UPDATE points
        SET visited=?
        WHERE id=?
        """,
            (
                int(visited),
                point_id
            )
        )

        self.conn.commit()


