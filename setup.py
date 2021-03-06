import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="imgurdownloader",
    version="0.1.0",
    author="Shyam Sunder",
    author_email="sgsunder1@gmail.com",
    description="Quickly download Imgur albums",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sgsunder/imgur-downloader",
    packages=setuptools.find_packages(),
    scripts=['bin/imgur-downloader'],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
)
