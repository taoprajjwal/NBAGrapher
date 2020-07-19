import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README=(HERE/"README.md").read_text()

setup(
    name="NBAGrapher",
    version="1.1.1",
    description="Graphing NBA player and team stats using matplotlib",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/taoprajjwal/NBAGrapher",
    author="Prajjwal Bhattarai",
    author_email="taoprajjwal@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["nbagrapher"],
    install_requires=["sportsreference", "matplotlib","pandas"],
    dependency_links=["https://github.com/taoprajjwal/basketball_reference_scraper/tarball/master"]
)