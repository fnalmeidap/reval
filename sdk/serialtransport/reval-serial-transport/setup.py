from setuptools import setup, find_packages

setup(
    name="reval-serial-transport",
    version="0.1.0",
    packages=find_packages(),
    requires=["pymavlink", "pyserial", "setuptools"],
)
