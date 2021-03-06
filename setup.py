from setuptools import setup, find_packages

version = '0.1'

setup(
    name='threedi-connector',
    version=version,
    packages=find_packages(),
    description='A 3Di client library',
    author='Jackie Leng',
    author_email='jackie.leng@nelen-schuurmans.nl',
    url='https://github.com/nens/threedi-connector',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    include_package_data=True,  # needed?
)
