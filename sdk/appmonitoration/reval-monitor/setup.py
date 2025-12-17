from setuptools import setup, find_packages

setup(
    name="revalmonitor",
    version="0.3.0",
    packages=find_packages(),
    requires=["protobuf", "setuptools"],
)
