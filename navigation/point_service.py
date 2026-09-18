#navigation/point_service.py
class PointService:

    def __init__(self, database):
        self.database = database
        self.points = []


    def normalize_sequences(self):

        self.points.sort(
            key=lambda p: p.sequence
        )

        for i, p in enumerate(
            self.points,
            start=1
        ):
            p.sequence = i


    def add_point(self, point):

        # Alapértelmezett visited flag,
        # ha még nincs az objektumon.
        if not hasattr(point, "visited"):
            point.visited = False

        self.points.append(point)

        self.normalize_sequences()

        print(
            "NEW POINT",
            point.latitude,
            point.longitude,
            point.sequence
        )


    def save_points(self, uids):

        selected = [
            p
            for p in self.points
            if p.uid in uids
        ]

        self.database.save_points(
            selected
        )


    def load_points(self):

        loaded = self.database.load_points()

        existing = {
            p.id: p
            for p in self.points
            if p.id is not None
        }


        for p in loaded:

            if p.id in existing:

                old = existing[p.id]

                old.latitude = p.latitude
                old.longitude = p.longitude
                old.time = p.time
                old.visited = p.visited
                old.sequence = p.sequence
                old.in_database = True

            else:

                # Biztosítsuk, hogy legyen
                # visited attribútum.
                if not hasattr(p, "visited"):
                    p.visited = False

                self.points.append(p)


        self.normalize_sequences()

    def set_visited(
        self,
        point_uid,
        visited
    ):

        # A frontend UUID (uid) alapján
        # megkeressük a memóriában lévő pontot.
        for p in self.points:

            if str(p.uid) == str(point_uid):

                # Memóriában frissítjük.
                p.visited = visited

                # Az adatbázisban már az SQLite
                # integer ID-ját használjuk.
                if p.id is not None:

                    self.database.set_visited(
                        p.id,
                        visited
                    )

                return


        raise ValueError(
            f"Point not found: {point_uid}"
        )


    def delete_points(self, uids):

        sql_delete = []
        new_list = []


        for p in self.points:

            if p.uid in uids:

                if p.id is not None:
                    sql_delete.append(p.id)

            else:

                new_list.append(p)


        if sql_delete:

            self.database.delete_points(
                sql_delete
            )


        self.points = new_list

        self.normalize_sequences()


    def get_next_unvisited_point(self):

        """
        Visszaadja a következő meglátogatandó
        pontot a sequence sorrend alapján.

        Csak olyan pontot ad vissza,
        amelynek visited értéke False.
        """

        self.normalize_sequences()

        for p in self.points:

            if not getattr(
                p,
                "visited",
                False
            ):
                return p

        return None

