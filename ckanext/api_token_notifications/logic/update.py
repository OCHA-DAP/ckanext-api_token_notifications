import ckan.plugins.toolkit as tk

from ckanext.api_token_notifications.helpers.token_expiration_helper \
        import find_expiring_api_tokens, send_emails_for_expiring_tokens


_check_access = tk.check_access
_get_or_bust = tk.get_or_bust
ValidationError = tk.ValidationError


def notify_users_about_api_token_expiration(context, data_dict):
    '''
    :param days_in_advance: how many days in advance we should look for expiring api tokens
    :type days_in_advance: int
    :param expires_on_specified_day: if True then we're looking only for api tokens that will expire on the
        specified day. Otherwise, we look for tokens that expire from now till the specified day.
    :type expires_on_specified_day: bool
    :return: number of api tokens that will expire
    '''
    _check_access('notify_users_about_api_token_expiration', context, {})
    days_in_advance, expires_on_specified_day = __extract_token_expiration_params(data_dict)

    model = context['model']
    session = context['model'].Session

    token_info_list, period_start_string, period_end_string = \
        find_expiring_api_tokens(model, session, days_in_advance, expires_on_specified_day)
    number_of_emails = send_emails_for_expiring_tokens(token_info_list)
    return {
        'start_date': period_start_string,
        'end_date': period_end_string,
        'emails_sent': number_of_emails,
    }


def __extract_token_expiration_params(data_dict):
    days_in_advance = _get_or_bust(data_dict, 'days_in_advance')
    try:
        days_in_advance = int(days_in_advance)
        expires_on_specified_day = data_dict.get('expires_on_specified_day') == 'true' \
                                   or data_dict.get('expires_on_specified_day') is True
    except ValueError:
        raise ValidationError('Limit must be a positive integer')
    return days_in_advance, expires_on_specified_day
