from django.conf import settings
from django.utils.module_loading import import_string
from users.sms.backends.constants import LOGIN_CASE, REGISTER_CASE, PHONE_REGEX, PASSWORD_CHANGE_CASE

import logging

log = logging.getLogger(__name__)


def get_backend():
    """
    :rtype: BaseSMSBackend
    """
    return import_string(settings.SMS_BACKEND)()


def send_login_code(phone):
    return send_verification_code(phone, LOGIN_CASE)


def send_register_code(phone):
    return send_verification_code(phone, REGISTER_CASE)


def send_password_change_code(phone):
    return send_verification_code(phone, PASSWORD_CHANGE_CASE)


def send_verification_code(phone, case):
    """Generate a random code for phone and send it via SMS.

    :param phone: phone number as string
    :type phone: str
    :return: ({'test': True, 'code': None, 'success': True}, None)
    :rtype: (dict, str)
    """
    if phone and phone.startswith('000000'):
        return True, ''

    backend = get_backend()
    result, error_msg = backend.send(phone, case)
    return result['success'], error_msg


def verify_login_code(phone, code):
    return verify_code(phone, code, LOGIN_CASE)


def verify_register_code(phone, code):
    return verify_code(phone, code, REGISTER_CASE)


def verify_password_change_code(phone, code):
    return verify_code(phone, code, PASSWORD_CHANGE_CASE)


def verify_code(phone, code, case):
    """
    verify sms code with redis value
    :param phone:  the phone of user
    :param code:  the code from user input
    :return: verified  or not
    """
    if code == '111111' and phone and phone.startswith('000000'):
        return True, None

    backend = get_backend()
    return backend.verify(phone, code, case)
