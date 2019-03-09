"""
book wish list
"""
from setuptools import setup, find_packages

setup(
    name='book_wish_list',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'sqlalchemy',
        'docker',
        'flask-login',
        'flask-restplus',
        'docker-compose'
    ]
)
