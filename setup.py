import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session='hack')
requirements = [str(ir.req) for ir in install_reqs]

setup(
    name='usersms',
    version="0.0.1",
    description='sms tools for user login/register',
    packages=['sms', 'sms.backends'],

    install_requires=requirements,
    zip_safe=False,
)
