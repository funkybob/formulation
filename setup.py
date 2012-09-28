from setuptools import setup, find_packages

VERSION = '1.0.4'

setup(
    name='formulation',
    version=VERSION,
    description='Django Form rendering tool',
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    url='http://github.com/funkybob/formulation',
    download_url='https://github.com/downloads/funkybob/formulation/formulation-%s.tar.gz' % VERSION,
    keywords=['django', 'forms', 'templates'],
    packages = find_packages(),
    zip_safe=False,
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
