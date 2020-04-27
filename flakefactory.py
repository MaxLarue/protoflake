"""
The flake factory initialize flake instances by instantiating their classes
then setting every attributes on them.
It produces one single flake at a time and expects references to already have been resolved
"""


class FlakeAttributeOverwriting(Exception):
    def __init__(self, instance, attr_name, attr_value, *args, **kwargs):
        super(*args, **kwargs)
        self.msg = 'Not settings attribute (%s, %s) on flake %s because that attribute already exists and is %s' % \
                   (attr_name, attr_value, instance, getattr(instance, attr_name))


class FlakeFactory(object):

    @staticmethod
    def build_flake(proto, flake_attrs):
        instance = proto()
        for attr_name, attr_value in flake_attrs.items():
            if hasattr(instance, attr_name):
                raise FlakeAttributeOverwriting(instance, attr_name, attr_value)
            setattr(instance, attr_name, attr_value)
        return instance
