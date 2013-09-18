from setuptools import setup, find_packages

setup(
    name='formulation',
    version='2.0.0',
    description='Django Form rendering tool',
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    keywords=['django', 'forms', 'templates'],
    packages = ['formulation',],
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
    ],
)
