from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kindle_notes',
    version='1.0.0',
    entry_points={
        'console_scripts': ['kindle-notes=kindle_notes.main:main'],
    },
    install_requires=['python-dateutil'],
    packages=find_packages(exclude=["tests", "tests.*"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/newswangerd/kindle-notes',
    description='Extract notes from kind clippings and convert them into markdown.'
)
