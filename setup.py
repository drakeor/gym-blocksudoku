from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='gym-blocksudoku-drakeor',
    version='0.0.1',
    author="Drakeor",
    author_email="me@drakeor.com",
    description="OpenAI Gym Environment for Block Sudoku",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/drakeor/gym-blocksudoku",
    packages=setuptools.find_packages(),
    install_requires=['gym', 'numpy']
)