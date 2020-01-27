class FlaskConf(object):
    def add_to_config(self, new_config):
        self.__dict__.update(new_config.__dict__)
        