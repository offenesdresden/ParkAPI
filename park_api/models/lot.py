import os
from park_api import env


class Lot:
    def __init__(self,
                 name,
                 id=None,
                 lot_type=None,
                 lng=None,
                 lat=None,
                 address=None,
                 total=None,
                 downloaded_at=None,
                 free=0,
                 forecast=False,
                 state="nodata"):
        self.name = name
        self.id = id
        self.lot_type = None
        self.lng = lng
        self.address = address
        self._total = total
        self.forecast = forecast
        self.state = state
        self.downloaded_at = downloaded_at
        self.forecast_path = os.path.join(env.APP_ROOT,
                                          "forecast_data",
                                          id + ".csv")
        self.has_forecast = os.path.isfile(self.forecast_path)

    def _coords(self):
        if self.lng is not None and self.lat is not None:
            return {'lng': self.lng, 'lat': self.lat}
        return None

    def as_json(self):
        return {
                "name": self.name,
                "total": self.total,
                "free": self.free,
                "coords": self._coords(),
                "state": self.state,
                "id": self.id,
                "lot_type": self.type,
                "address": self.address,
                "forecast": self.forecast,
                "region": self.region
        }
