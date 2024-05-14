import yaml
from pathlib import Path

months = ['ZERO', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

class ConfigurationManager:
    def __init__(self):
        self.path = Path(__file__).parents[2].joinpath('configuration.yaml')

        with open(self.path, 'r') as file:
            config = yaml.safe_load(file)

        self.configuration = config
        self.screen_wd = config['screen-working-directory']
        self.schedule_wd = config['schedule-working-directory']
        self.month = config['current']['month']
        self.year = config['current']['year']
        self.screen_categories = config['screen-categories']
        self.schedule_categories = config['schedule-categories']
        self.has_notion = config['notion-integration-enabled']

    def rewrite_configuration(self):
        with open(self.path, 'w') as file:
            yaml.dump(self.configuration, file, sort_keys=False)
        
    def get_date(self): 
        return f'{months[self.month]} {self.year}'

    def next_month(self):
        if self.month < 12: 
            self.configuration['current']['month'] = self.month + 1

        if self.month == 12: 
            self.configuration['current']['month'] = 1
            self.configuration['current']['year'] = self.year + 1

        self.month = self.configuration['current']['month']
        self.year = self.configuration['current']['year']

        self.rewrite_configuration()

    def prev_month(self):
        if self.month > 1:
            self.configuration['current']['month'] = self.month - 1

        if self.month == 1: 
            self.configuration['current']['month'] = 12
            self.configuration['current']['year'] = self.year - 1

        self.month = self.configuration['current']['month']
        self.year = self.configuration['current']['year']

        self.rewrite_configuration()