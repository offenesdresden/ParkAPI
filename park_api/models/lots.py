from datetime import datetime
from park_api import util


class Lots():
    def __init__(self):
        self._lots = {}

    def append(self, lot):
        self._lots[lot.id] = lot

    def __setitem__(self, index, value):
        self._lots[index] = value

    def __getitem__(self, index):
        return self._lots[index]

    def __delitem__(self, index):
        del self._lots[index]

    def __len__(self):
        return len(self._lots)

    def __iter__(self):
        for lot in self._lots.values():
            yield lot

    def save(self, cursor):
        """Persist lots to database."""
        inserts = []
        downloaded_at = util.utc_now()
        for lot in self._lots.values():
            sql = "(%s, %s, %s, %s)"
            values = (lot.id, lot.free, lot.updated_at, downloaded_at)
            inserts.append(cursor.mogrify(sql, values))
        insert_sql = """
        INSERT INTO free_lots(lot_id, free, updated_at, downloaded_at) VALUES
        """
        cursor.execute(insert_sql + ",".join(inserts))

    def load(self, cursor):
        """Load lastet scraped lot information from database."""
        sql = """
        SELECT DISTINCT ON (fl.lot_id)
                            fl.lot_id,
                            fl.free,
                            Coalesce(l.total, l.total_seen),
                            Coalesce(fl.updated_at, fl.downloaded_at)
            FROM free_lots as fl
            WHERE lot_id in %s
            LEFT OUTER JOIN lots as l ON (fl.lot_id = l.id)
            GROUP BY lot_id
            ORDER BY downloaded_at DESC
        """
        cursor.execute(sql, (self._lots.keys(),))
        for row in cursor:
            id, free, total, updated_at = row
            lot = self._lots[id]
            lot.free = free
            lot.total = total
            lot.updated_at = updated_at

    def as_json(self):
        lots = []
        last_updated = datetime.fromtimestamp(0)
        for lot in self._lots.values():
            lots.append(lot.as_json())
            if lot.updated_at > last_updated:
                last_updated = lot.updated_at
        return {
                "last_updated": last_updated,
                "lots": lots
        }
