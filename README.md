# qx-community

my django project community

### Install:

    pip install -e git://github.com/qx-oo/qx-community.git@master#egg=qx-community

### Usage:

depends:

    qx-base >= 1.0.7

settings.py:

    INSTALLED_APPS = [
        ...
        'qx_base.qx_core',
        'qx_base.qx_rest',
        'qx_base.qx_user',
        'qx_community',
        ...
    ]