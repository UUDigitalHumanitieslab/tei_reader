from setuptools import setup, find_packages

setup(
    name='tei_reader',
    python_requires='>=3.6, <4',
    version='0.0.4',
    description='TEI Reader',
    author='Sheean Spoel (Digital Humanities Lab, Utrecht University)',
    author_email='s.j.j.spoel@uu.nl',
    url='https://github.com/UUDigitalHumanitieslab/tei_reader',
    license='MIT',
    packages=['tei_reader'],
    zip_safe=False,
    install_requires=['beautifulsoup4', 'lxml']
)
