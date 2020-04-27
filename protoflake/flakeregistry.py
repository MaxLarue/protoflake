"""
The flake registry holds already built flake instances.
Right now it is only a mapping.
"""


class FlakeAlreadyExist(Exception):
    def __init__(self, flake_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = 'Trying to register a flake with id %s which already exists' % flake_id


class FlakeRegistry(object):

    def __init__(self):
        super().__init__()
        self.registry = {}

    def has(self, flake_id: str):
        return flake_id in self.registry

    def get(self, flake_id):
        return self.registry[flake_id]

    def set(self, flake_id, flake):
        if self.has(flake_id):
            raise FlakeAlreadyExist(flake_id)
        self.registry[flake_id] = flake
