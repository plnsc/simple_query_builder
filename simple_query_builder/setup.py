from setuptools import find_packages, setup

VERSION = "0.0.0"
DESCRIPTION = "Tools to help building SQL"
LONG_DESCRIPTION = "Provide simple tools to help building SQL queries"

setup(
    name="simple_query_builder",
    version=VERSION,
    author="Paulo Nascimento",
    author_email="<paulornasc@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["coverage", "pytest"],
    keywords=["python", "simple", "sql", "builder"],
    classifiers=[],
)
