from csv import reader

with open('csis_config.txt', 'r') as data:
    reader = reader(data, delimiter="=")
    configs = {}
    for config in reader:
        print(config)
        try:
            configs[config[0]] = config[1]
        except IndexError:
            pass

bool_dict = {'True': True, 'False': False}

configs['test'] = bool_dict[configs['test']]


class CSISConfigs:
    def __init__(self):
        self.configs = configs
        self.test = configs['test']
        if self.test:
            self.data_path = self.configs['test_data_path']
        else:
            self.data_path = self.configs['data_path']
