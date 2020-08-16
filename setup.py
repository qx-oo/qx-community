from setuptools import find_packages, setup


setup(
    name='qx-community',
    version='1.0.0',
    author='Shawn',
    author_email='q-x64@live.com',
    url='https://github.com/qx-oo/qx-community/',
    description='Django basic community apps.',
    long_description=open("README.md").read(),
    packages=find_packages(exclude=["qx_test"]),
    install_requires=[
        'cryptography>=2.9',
        'django-filter>=2.2',
    ],
    python_requires='>=3.8',
    platforms='any',
)
