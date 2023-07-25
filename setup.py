import versioneer
from setuptools import setup, find_packages

requirements = [
    'click>=7.0',
    'pandas>=1.0.0',
    'pyyaml',
    'pysam'
]

setup(
    name='cellranger_utils',
    packages=find_packages(),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='python utilities for cellranger',
    author='Diljot Grewal',
    author_email='diljot.grewal@gmail.com',
    entry_points={
        'console_scripts': [
            'cellranger_utils = cellranger_utils.cli:cli'
        ]
    },
    install_requires=requirements,
    package_data={'': ['*.py', '*.R', '*.npz', "*.yaml", "data/*", "*.sh"]}
)
