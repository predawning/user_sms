import logging
from django.core.cache import cache
from django.utils.crypto import get_random_string

from .constants import PHONE_PATTERN, SMS_SIGN
from .constants import TEXT_VERIFICATION_LENGTH, TEMPLATES

log = logging.getLogger(__name__)


class BaseSMSBackend:
    name = 'mock_key'
    tried_count = 6
    timeout = 60
    sign = SMS_SIGN

    def get_key(self, phone, case):
        return "%s_%s_%s"% (self.name, phone, case)

    def set_code(self, phone, code, case):
        cache.set(self.get_key(phone, case), code, timeout=self.timeout)

    def get_code(self, phone, case):
        return cache.get(self.get_key(phone, case))

    def rm_code(self, phone, case):
        key = self.get_key(phone, case)
        cache.delete(key)
        self.clear_count(key)

    def sign_message(self, content):
        content += self.sign
        return content

    def get_tried_count(self, key):
        count_key = key + 'count'
        return cache.get(count_key, 0)

    def set_tried_count(self, key, count):
        count_key = key + 'count'
        cache.set(count_key, count, timeout=self.timeout)

    def incr_count(self, key):
        count_key = key + 'count'
        cache.incr(count_key)

    def clear_count(self, key):
        count_key = key + 'count'
        cache.delete(count_key)

    def send(self, phone, case):
        """
        :param phone: phone number as string
        :type phone: str
        :return: ({'test': True, 'code': None, 'success': True}, None)
        :rtype: (dict, str)
        """
        result = {'test': False, 'success': False}

        phone_num = self.strip_phone_prefix(phone)
        log.info("Sending verification code to %s", phone_num)
        if phone_num:
            valid, error_msg = self.validate_phone(phone_num)
            if not valid:
                return {'success': False, 'code': ''}, error_msg

            code = self.get_code(phone_num, case)
            if not code:
                code = get_random_string(TEXT_VERIFICATION_LENGTH, '0123456789')

            success, error_msg = self._send_code(phone, code, case)

            result.update({'success': success, 'code': code})
            if success:
                log.debug('{} sent a message {}'.format(self.name, phone_num))
                # store the code in redis as well
                self.set_code(phone_num, code, case)
            else:
                log.error('{} send {} error {}'.format(self.name, phone_num, error_msg))
        else:
            error_msg = 'Wrong phone format: {}'.format(phone_num)

        return result, error_msg

    def _send_code(self, phone, code, case):
        """
        subclass must implement it
        :param phone:
        :param code:
        :param case:
        :return:
        """
        raise NotImplementedError

    def verify(self, phone, code, case):
        """Compare the verification code to sent ones.

        :type phone: string
        :type code: string
        """
        key = self.get_key(phone, case)
        tried_count = self.get_tried_count(key)
        if tried_count > self.tried_count:
            return False, 'tried too many times'
        else:
            if tried_count == 0:
                self.set_tried_count(key, 1)
            else:
                self.incr_count(key)
        saved_code = self.get_code(phone, case)
        verified = saved_code == code
        if verified:
            self.rm_code(phone, case)
            return verified, None
        else:
            return verified, '%s code verify failed' % case


    def strip_phone_prefix(self, phone_num):
        """Strip "+86" from phone number, if exists

        :type phone_num: str
        :return: local phone number if correct format, or None
        """
        # FIXME more accurate check
        if phone_num.startswith('+86'):
            return phone_num.replace('+86', '')
        if len(phone_num) != 11:
            return None
        return phone_num

    def validate_phone(self, phone_num):
        if not PHONE_PATTERN.match(phone_num):
            return False, 'INVALID_PHONE'
        else:
            return True, 'VALID_PHONE'
