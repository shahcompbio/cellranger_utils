import versioneer
from setuptools import setup, find_packages

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
    package_data={'': ['*.py', '*.R', '*.npz', "*.yaml", "data/*", "*.sh"]}
)
