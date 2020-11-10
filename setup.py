from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
    name='gym-blocksudoku',
    version='0.0.1',
    install_requires=['gym', 'numpy']
)