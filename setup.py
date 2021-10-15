from setuptools import setup

setup(
    name='msa_test',
    version='0.1.0',    
    description='An example Python MSA package',
    author='Nicolas Carrez',
    author_email='nicolas.carrez@gmail.com',
    license='BSD 2-clause',
    packages=['msa_test'],
    package_data={'msa_test': ['static/*']},
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
