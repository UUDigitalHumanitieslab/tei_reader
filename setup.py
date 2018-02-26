from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='tei_reader',
    version='0.0.2',
    description='TEI Reader',
    long_description=readme,
    author='Sheean Spoel',
    author_email='s.j.j.spoel@uu.nl',
    url='https://github.com/UUDigitalHumanitieslab/tei_reader',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
