import bitcheck

from setuptools import setup

with open('README.md', 'r') as f:
    readme = f.read().decode('utf-8')

setup(
    name='bitcheck',
    version=bitcheck.__version__,
    description='Bitcoin profitability check',
    entry_points = {
        "console_scripts": ['bitcheck = bitcheck.__main__:main']
    },
    long_description=readme,
    author='Victor Cinaglia',
    author_email='victor@cinaglia.com',
    url='https://github.com/cinaglia/bitcheck',
    packages=['bitcheck'],
    license='Public Domain',
)