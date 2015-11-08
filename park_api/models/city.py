class City:
    def __init__(self, name,
                 id=None,
                 lng=None,
                 lat=None,
                 url=None,
                 source=None,
                 active_support=False):
        self.name = name
        self.id = id
        self.lat = lat
        self.lng = lng
        self.url = url
        self.source = source
        self.active_support = active_support

    def _coords(self):
        if self.lng is not None and self.lat is not None:
            return {'lng': self.lng, 'lat': self.lat}
        return None

    def as_json(self):
        return {
                "name": self.name,
                "coords": self._coords,
                "source": self.source,
                "url": self.url,
                "active_support": self.active_support
        }
