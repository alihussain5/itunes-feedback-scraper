from distutils.core import setup


setup(
    name='iscraper',
    version='1.0.0',
    packages=['iscraper'],
    package_dir={
        'iscraper': 'scraper',
    },

    author='allawi',
    author_email='me@alihussa.in',

    install_requires=[
        'requests>=2.3.0',
    ]
)
