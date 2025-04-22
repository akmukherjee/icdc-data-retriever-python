from setuptools import setup, find_packages

setup(
    name="icdc-data-retriever",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "aiohttp",
        "beautifulsoup4",
        "python-dotenv",
    ],
)
