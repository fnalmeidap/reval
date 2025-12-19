from setuptools import setup, find_packages

setup(
    name="reval-monitor",
    version="0.4.0",
    packages=find_packages(),
    requires=["protobuf", "setuptools"],
)
