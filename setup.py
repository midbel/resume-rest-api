from setuptools import setup

setup(
    name='resume',
    packages=['resume'],
    include_package_data=True,
    install_requires=[
        'flask',
        'sqlalchemy',
        'PyJWT',
    ],
)
