from setuptools import setup, find_packages

setup(
    name="aisecurity",
    version="0.9a",
    description="CSII AI facial recognition.",
    long_description=open("README.md", encoding="utf-8").read(),
    url="https://github.com/orangese/aisecurity",
    author="Ryan Park, Liam Pilarski",
    author_email="22parkr@millburn.org, 22pilarskil@millburn.org",
    license=None,
    python_requires=">=3.5.0",
    install_requires=["adafruit-circuitpython-charlcd", "tensorflow==1.15.0", "keras", "matplotlib", "mysql-connector-python",
                      "Pyrebase", "pycryptodome", "requests", "scikit-learn", "mtcnn"],
    scripts=["bin/drop.sql", "bin/make_config.sh", "bin/make_keys.sh"],
    packages=find_packages(),
    zip_safe=False
)
