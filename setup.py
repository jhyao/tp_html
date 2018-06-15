import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tp_html",
    version="0.0.2",
    author="jhyao",
    author_email="yaojinhonggg@gmail.com",
    description="Get data from html",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jhyao/tp_html",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)