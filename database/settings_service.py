# database/settings_service.py


class SettingsService:

    def __init__(self, database):

        self.database = database


    def get_setting(self, setting_name):

        return self.database.get_setting(
            setting_name
        )


    def set_setting(self, setting_name, value):

        self.database.set_setting(
            setting_name,
            value
        )
