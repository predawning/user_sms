import logging

from .base import BaseSMSBackend

log = logging.getLogger(__name__)


class DummySMSBackend(BaseSMSBackend):

    def send(self, phone, case):
        result = {'test': False, 'success': False}

        phone_num = self.strip_phone_prefix(phone)
        if phone_num:
            valid, error_msg = self.validate_phone(phone_num)
            if not valid:
                log.error('{} msg: {}'.format(phone_num, error_msg))
                return {'success': False, 'code': ''}, error_msg

            result = {'test': True, 'code': None, 'success': True}
            error_msg = None
        else:
            error_msg = 'Wrong phone format: {}'.format(phone_num)
        return result, error_msg


    def verify(self, phone, code, case):
        if code == '111111':
            return True, None
        return False, 'This is a testing version. Please use code 111111.'
