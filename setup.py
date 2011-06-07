import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'django-html-filter',
    version = '0.1',
    license = 'BSD',
    description = 'Filter HTML output from Django views.',
    long_description = read('README.rst'),
    author = 'Jeff Kistler',
    author_email = 'jeff@jeffkistler.com',
    url = 'https://github.com/jeffkistler/django-html-filter/',
    packages = ['django_html_filter'],
    package_dir = {'': 'src'},
    install_requires = ['html5lib==0.90'],
    classifiers = [
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
