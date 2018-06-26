# -*- coding: utf-8 -*-
import uuid
import logging
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import RpcRequest
from aliyunsdkcore.profile import region_provider

from django.conf import settings
from .base import BaseSMSBackend
from .constants import LOGIN_CASE, REGISTER_CASE, PASSWORD_CHANGE_CASE


log = logging.getLogger(__name__)

REGION = "cn-beijing"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

class SendSmsRequest(RpcRequest):

    def __init__(self):
        RpcRequest.__init__(self, 'Dysmsapi', '2017-05-25', 'SendSms')

    def get_TemplateCode(self):
        return self.get_query_params().get('TemplateCode')

    def set_TemplateCode(self,TemplateCode):
        self.add_query_param('TemplateCode',TemplateCode)

    def get_PhoneNumbers(self):
        return self.get_query_params().get('PhoneNumbers')

    def set_PhoneNumbers(self,PhoneNumbers):
        self.add_query_param('PhoneNumbers',PhoneNumbers)

    def get_SignName(self):
        return self.get_query_params().get('SignName')

    def set_SignName(self,SignName):
        self.add_query_param('SignName',SignName)

    def get_ResourceOwnerAccount(self):
        return self.get_query_params().get('ResourceOwnerAccount')

    def set_ResourceOwnerAccount(self,ResourceOwnerAccount):
        self.add_query_param('ResourceOwnerAccount',ResourceOwnerAccount)

    def get_TemplateParam(self):
        return self.get_query_params().get('TemplateParam')

    def set_TemplateParam(self,TemplateParam):
        self.add_query_param('TemplateParam',TemplateParam)

    def get_ResourceOwnerId(self):
        return self.get_query_params().get('ResourceOwnerId')

    def set_ResourceOwnerId(self,ResourceOwnerId):
        self.add_query_param('ResourceOwnerId',ResourceOwnerId)

    def get_OwnerId(self):
        return self.get_query_params().get('OwnerId')

    def set_OwnerId(self,OwnerId):
        self.add_query_param('OwnerId',OwnerId)

    def get_SmsUpExtendCode(self):
        return self.get_query_params().get('SmsUpExtendCode')

    def set_SmsUpExtendCode(self,SmsUpExtendCode):
        self.add_query_param('SmsUpExtendCode',SmsUpExtendCode)

    def get_OutId(self):
        return self.get_query_params().get('OutId')

    def set_OutId(self,OutId):
        self.add_query_param('OutId',OutId)

acs_client = AcsClient(settings.ALIYUN_ACCESS_KEY_ID, settings.ALIYUN_ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


# Aliyun SMS template code is defined in advance
TEMPLATES = {
    LOGIN_CASE: 'SMS_132780027',
    REGISTER_CASE: 'SMS_132780025',
    PASSWORD_CHANGE_CASE: 'SMS_132780024',
}

class AliyunClient:

    def send_code(self, mobile, code, sign, template_code):
        business_id = uuid.uuid1()
        params = json.dumps({"code": code})
        try:
            response = self.send_sms(business_id, mobile, sign, template_code, params)
            result = json.loads(response)
        except Exception as e:
            log.exception('failed to send sms by aliyun')
            return False, 'System error, please check log'
        else:
            if result['Code'] == 'OK':
                return True, ''
            log.warn('failed to sent sms for %s: %s', mobile, str(result))
            return False, '{Code}:{Message}'.format(**result)

    def send_sms(self, business_id, phone_numbers, sign_name, template_code, template_param=None):

        # https://help.aliyun.com/document_detail/55491.html?spm=5176.10629532.106.3.2e8a1cbeB67GIq
        smsRequest = SendSmsRequest()

        # 申请的短信模板编码,必填
        smsRequest.set_TemplateCode(template_code)

        # 短信模板变量参数
        if template_param is not None:
            smsRequest.set_TemplateParam(template_param)

        # 设置业务请求流水号，必填。
        smsRequest.set_OutId(business_id)

        # 短信签名
        smsRequest.set_SignName(sign_name)

        # 短信发送的号码列表，必填。
        smsRequest.set_PhoneNumbers(phone_numbers)

        # 调用短信发送接口，返回json
        smsResponse = acs_client.do_action_with_exception(smsRequest)

        return smsResponse.decode('utf-8')


class AliyunBackend(BaseSMSBackend):

    name = 'aliyun'

    def _send_code(self, phone_num, code, case):
        """
        :param phone: phone number as string
        :type phone: str
        :return: ({'test': True, 'code': None, 'success': True}, None)
        :rtype: (dict, str)
        """
        template_code = TEMPLATES.get(case)
        return AliyunClient().send_code(phone_num, code, self.sign, template_code)


def test_send():
    import logging
    import http.client as http_client
    from .constants import LOGIN_CASE
    from django.conf import settings
    assert settings.DEBUG

    http_client.HTTPConnection.debuglevel = 1

    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    AliyunBackend().send('15810469596', case=LOGIN_CASE)

if __name__ == '__main__':
    test_send()




