from setuptools import setup, find_packages

setup(
    name='cryptography',
    version='0.2.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'cryptography = src.cli.main:main',
        ],
    },
)
