from setuptools import setup, find_packages

setup(
    name='formulation',
    version='1.0.2',
    description='Django Form rendering tool',
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    url='http://github.com/funkybob/formulation',
    download_url='https://github.com/downloads/funkybob/formulation/formulation-1.0.1.tar.gz',
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
