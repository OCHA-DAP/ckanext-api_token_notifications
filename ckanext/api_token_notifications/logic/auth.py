import ckan.plugins.toolkit as tk

_ = tk._


def notify_users_about_api_token_expiration(context, data_dict):
    return {'success': False, 'msg': _('Only sysadmins can view user permission page')}
