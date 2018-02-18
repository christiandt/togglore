import ConfigParser
import datetime


class Config(object):
    def __init__(self, api_key=None, work_hours_per_day=8.4, excluded_days=[], user_id=1, workspace=1):
        self.api_key = api_key
        self.work_hours_per_day = work_hours_per_day
        self.excluded_days = excluded_days
        self.user_id = user_id
        self.workspace = workspace

    def write_to_file(self, path):
        cfg = ConfigParser.ConfigParser()

        cfg.add_section('Authentication')
        cfg.set('Authentication', 'API_KEY', self.api_key)

        with open(path, 'w') as configfile:
            cfg.write(configfile)

    @classmethod
    def read_from_file(cls, path):
        cfg = ConfigParser.ConfigParser()
        cfg.read(path)

        api_key = cfg.get('Authentication', 'API_KEY')
        work_hours = cfg.get('Work Hours', 'hours_per_day')
        excluded_days_string = cfg.get('Work Hours', 'excluded_days')
        user_id = cfg.get('User Info', 'id')
        workspace = cfg.get('User Info', 'workspace')

        day_strings = excluded_days_string.split(',')
        days = []

        for day_string in day_strings:
            days.append(datetime.datetime.strptime(day_string, "%Y.%m.%d").date())

        return cls(api_key=api_key, work_hours_per_day=float(work_hours), excluded_days=days, user_id=user_id,
                   workspace=workspace)
