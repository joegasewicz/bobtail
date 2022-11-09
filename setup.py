from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="bobtail",
    version="0.0.1",
    description="A little Python http framework",
    packages=["bobtail"],
    py_modules=["bobtail"],
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joegasewicz/bobtail",
    author="Joe Gasewicz",
    author_email="joegasewicz@gmail.com",
)
