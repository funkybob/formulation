from setuptools import setup

setup(
    name='formulation',
    version='2.0.12',
    description='Django Form rendering tool',
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    keywords=['django', 'forms', 'templates'],
    packages = ['formulation', 'formulation.templatetags'],
    package_data = {
        'formulation': ['templates/formulation/*.form',],
    },
    zip_safe=False,
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
