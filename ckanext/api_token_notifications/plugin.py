import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.api_token_notifications.logic.update as update
import ckanext.api_token_notifications.logic.auth as auth

from ckanext.api_token_notifications.helpers.token_creation_notification_helper import send_email_on_token_creation


class ApiTokenNotificationsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IApiToken, inherit=True)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        # toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'api_token_notifications')


    # IActions
    def get_actions(self):
        return {
            'notify_users_about_api_token_expiration': update.notify_users_about_api_token_expiration,
        }

    # IAuthFunctions
    def get_auth_functions(self):
        return {
            'notify_users_about_api_token_expiration': auth.notify_users_about_api_token_expiration,
        }

    # IApiToken
    def postprocess_api_token(self, data, jti, data_dict):
        send_email_on_token_creation(data_dict.get('user'), data_dict.get('name'), data.get('exp'))
        return data
