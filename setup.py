from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="toad_bot",
    version="0.0.16",
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),
)