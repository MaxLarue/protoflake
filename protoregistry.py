"""
The proto registry allows us to only load proto classes once.
It'll then store them and make them available through the get method
"""
import importlib
import inspect


class ProtoModuleNotFound(ImportError):
    def __init__(self, module_name, class_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = 'Unable to import module %s, while trying to retrieve class %s' % (module_name, class_name)


class ProtoClassNotFound(ImportError):
    def __init__(self, module_name, class_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = 'Unable to find class %s in module %s' % (module_name, class_name)


class ProtoClassNotAClass(ImportError):
    def __init__(self, module_name, class_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = 'Found attribute %s in module %s, but it is not a class' % (module_name, class_name)


class ProtoRegistry(object):

    def __init__(self):
        self.module_registry = {}
        self.class_registry = {}

    def get(self, module: str, klass: str) -> object:
        full_name = module + klass
        if full_name not in self.class_registry:
            self.class_registry[full_name] = self.load_proto(module, klass)
        return self.class_registry[full_name]

    def load_proto(self, module_name: str, klass_name: str) -> object:
        if module_name in self.module_registry:
            module = self.module_registry[module_name]
        else:
            try:
                module = importlib.import_module(module_name)
            except ImportError:
                raise ProtoModuleNotFound(module_name, klass_name)
            self.module_registry[module_name] = module
        try:
            klass = getattr(module, klass_name)
            if not inspect.isclass(klass):
                raise ProtoClassNotAClass(module_name, klass_name)
            return klass
        except AttributeError:
            raise ProtoClassNotFound(module_name, klass_name)
