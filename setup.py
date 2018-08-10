from setuptools import setup, find_packages

# read the contents of README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tei_reader',
    python_requires='>=3.6, <4',
    version='0.0.13',
    description='TEI Reader',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sheean Spoel (Digital Humanities Lab, Utrecht University)',
    author_email='s.j.j.spoel@uu.nl',
    url='https://github.com/UUDigitalHumanitieslab/tei_reader',
    license='MIT',
    packages=['tei_reader', 'tei_reader.models', 'tei_reader.transform'],
    package_data={'tei_reader.transform':['*']},
    zip_safe=False,
    install_requires=['beautifulsoup4', 'lxml']
)
