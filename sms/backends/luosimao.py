import logging

import requests
from django.conf import settings
from django.utils.crypto import get_random_string

from .base import BaseSMSBackend
from .constants import TEXT_VERIFICATION_LENGTH, TEMPLATES

log = logging.getLogger(__name__)


class LSMClient:
    api_key = getattr(settings, 'LUOSIMAO_API_KEY')

    def check_api_key(self):
        if self.api_key is None:
            raise TypeError('API Key has to be set before any API calls')

    def send_sms(self, mobile, message):
        """To send SMS to specified mobile number.

        :param str mobile: mobile number to send the SMS to
        :param str message: the message
        :return: (True, None) or (False, err_msg)
        :rtype: (Boolean, None or str)
        """
        self.check_api_key()
        if not isinstance(mobile, str):
            raise TypeError('mobile has to be a string')
        if not isinstance(message, str):
            raise TypeError('message has to be a string')
        # TODO: verify mobile's validity of a phone number in China
        resp = requests.post(settings.LUOSIMAO_URL + 'send.json',
                             auth=('api', 'key-' + self.api_key),
                             data={'mobile': mobile, 'message': message})
        resp = resp.json()
        if resp['error'] == 0:
            return True, None
        return False, resp['msg']


class LuosimaoSMSBackend(BaseSMSBackend):
    name = 'luosimao'
    sign = '【铁壳测试】'

    def _send_code(self, phone_num, code, case):
        """
        :param phone: phone number as string
        :type phone: str
        :return: ({'test': True, 'code': None, 'success': True}, None)
        :rtype: (dict, str)
        """
        content = TEMPLATES.get(case).format(code)
        message = self.sign_message(content)
        client = LSMClient()
        return client.send_sms(phone_num, message)


def test_send():
    import logging
    import http.client as http_client
    from .constants import LOGIN_CASE
    assert settings.DEBUG

    http_client.HTTPConnection.debuglevel = 1

    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    LuosimaoSMSBackend().send('15810469596', case=LOGIN_CASE)

if __name__ == "__main__":
    test_send()
