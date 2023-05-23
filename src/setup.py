from setuptools import setup, find_packages

setup(
    name='corebase',
    version='1.0',
    author='Vladlen Li',
    description='Core base',
    install_requires=[],
    license="MIT",
    packages=find_packages(
        include=['core_entity', 'core_repository', 'core_logger', 'core_entity.protocol']),
)