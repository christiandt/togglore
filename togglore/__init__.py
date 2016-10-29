from togglore import toggl
from togglore import utils


class Togglore(object):
    def __init__(self, api_token):
        self.toggle = toggl.TogglClient(api_token)

    def diff(self, date_range):
        actual_hours = utils.sum_time_of_entries(self.toggle.time_entries(date_range))
        expected_hours = utils.WorkTimeCalculator().time_to_work_in_range(date_range)

        return actual_hours, expected_hours
