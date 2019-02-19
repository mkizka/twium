from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    setup(
        name='twium',
        version='0.1.1',
        description='Seleniumを使ったpython-twitter風ラッパー',
        author='Compeito',
        author_email='com0806peito@icloud.com',
        url='https://github.com/Compeito/twium',
        license='MIT',
        packages=find_packages(where='.'),
        install_requires=[p.strip() for p in f.read().split('\n')],
    )
