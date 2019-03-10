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
        'flask-sqlalchemy',
        'flask-restplus',
        'psycopg2',
        'passlib',
        'sqlalchemy_utils',
        'docker-compose'
    ],
    test_require=[
        'pytest',
        'pytest-cov',
        'pytest-flask',
        'mock',
        'pyquery'
    ]
)
