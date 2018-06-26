import re
from django.conf import settings

# Length of verification code
TEXT_VERIFICATION_LENGTH = 6

# Template of the sms text content's
SMS_SIGN = "基站"

LOGIN_VERIFY_TEMPLATE = "登录验证码: {0} "
REGISTER_VERIFY_TEMPLATE = "注册验证码: {0}"
PASSWORD_CHANGE_TEMPLATE = "修改密码验证码: {0}"

LOGIN_CASE = 'LOGIN_CASE'
REGISTER_CASE = 'REGISTER_CASE'
PASSWORD_CHANGE_CASE = 'PASSWORD_CHANGE_CASE'

TEMPLATES = {
    LOGIN_CASE: LOGIN_VERIFY_TEMPLATE,
    REGISTER_CASE: REGISTER_VERIFY_TEMPLATE,
    PASSWORD_CHANGE_CASE: PASSWORD_CHANGE_TEMPLATE,
}

# let 00000012345 as phone number for internal testing purpose also
if settings.DEBUG:
    PHONE_REGEX = r'^1[3|4|5|7|8][0-9]\d{8}$|^0{6}\d{5}$'
else:
    PHONE_REGEX = r'^1[3|4|5|7|8][0-9]\d{8}$'
PHONE_PATTERN = re.compile(PHONE_REGEX)