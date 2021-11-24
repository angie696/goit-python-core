from setuptools import setup, find_packages


setup(
    name="clean_folder",
    version="1.0",
    author="Anzhelika",
    packages=find_packages(),
    description="clean folder script",
    entry_points={
        'console_scripts': ['clean-folder=clean_folder.clean:main'],
    },
)
