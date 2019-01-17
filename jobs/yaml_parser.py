import yaml


class YamlParser:

    def __init__(self):
        # Open yaml file
        self.date = None
        try:
            yaml_config = yaml.load(open('config/googleTrends.yaml'))
        except:
            print("No googleTrends yaml in config")
            raise EnvironmentError
        print(yaml_config)

        if (yaml_config.get('date_begin') is not None) and (yaml_config.get('date_end') is not None):
            self.date = yaml_config.get('date_begin') + ' ' + yaml_config.get('date_end')
        else:
            self.date = yaml_config.get('date_pattern') if yaml_config.get('date_pattern') is not None else 'now 4-H'
            print(self.date)

        self.geo = yaml_config.get('geo') if yaml_config.get('geo') is not None else ''

        if yaml_config.get('terms') is None:
            print('No terms')
            exit()
        self.terms = yaml_config.get('terms')

