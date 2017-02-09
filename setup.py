import os
from setuptools import find_packages, setup

# with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
#     README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

install_requires = [
    'django>=1.10',
    'mysql-python==1.2.5',
    'pillow==4.0.0',
    'social-auth-app-django==1.0.1',
]
develop_requires = [
    'pdbpp',
    'ipython',
    'readline',
    'mock',
]

setup(
    name='apof',
    # version=__import__('apof').__version__,
    version='dev',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    license='BSD License',  # example license
    description='',
    long_description='',
    url='',
    author='',
    author_email='',
    install_requires=install_requires,
    extras_require={
        'develop': develop_requires,
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Python Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2.12',
    ],
)
