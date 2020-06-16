
class ReloadWrapper():
    def __init__(self):
        self.updateRequired = False
        self.unit = None

    def reload(self):
        self.updateRequired = self.unit is not None

    def _reload(self):
        import intcode
        importlib.reload(intcode)
        self.unit = intcode.Code()
        self.updateRequired = False

    def _load(self):
        try:
            import intcode
            self.unit = intcode.Code()
            return True
        except Exception as e:
            logger.error(f'Error loading: {e}')

        return False

    def get_unit(self):
        if self.unit is None:
            result = self._load()
            if not result:
                return None

        if self.updateRequired:
            self._reload()

        return self.unit

    def get_test_msg(self):
        if self.unit is None:
            result = self._load()
            if not result:
                return None

        if self.updateRequired:
            self._reload()

        return self.unit.test_msg()


def load_config():
    with open("config.yml") as f:
        try:
            g_config = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            return None

    return g_config
