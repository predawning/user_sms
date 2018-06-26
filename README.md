# user_sms
a sms utils for user login/register use case

# settings

    # luosimao sms key
    LUOSIMAO_URL = 'https://sms-api.luosimao.com/v1/'
    LUOSIMAO_API_KEY = ''

    # aliyun sms access key
    ALIYUN_ACCESS_KEY_ID = ''
    ALIYUN_ACCESS_KEY_SECRET = ''

    # the active sms backend
    # dummy version is just silent the sms sending, but verify with the magic code 111111
    # it only used for test environment
    
    # aliyun version and luosimao version are for product environment
    SMS_BACKEND = 'sms.backends.dummy.DummySMSBackend'

    if need to share the user code in cluster still need to config the redis cache
    e.g.
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://localhost:6379/0",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
    }    

# usage
    from sms import send_login_code, verify_login_code
    succeed, err_msg = send_login_code(phone)
    if succeed:
        verify_login_code(phone, code)
    else:
        return err_msg
