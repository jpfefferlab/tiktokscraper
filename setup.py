from setuptools import setup, find_packages

setup(
    name="tiktokscraper",            # Name of your package
    version="0.1.0",                 # Version of your package
    description="A package to collect TikTok videos, comments and user information, perform keyword search and collect the followers, followings and videos of a user.",  # Short description
    long_description=open("README.rst").read(),  # Long description from README
    long_description_content_type="text/x-rst",  # Format of the long description
    author="Angelina Voggenreiter",              # Your name
    author_email="angelina.voggenreiter@tum.de",  # Your email
    url="https://github.com/jpfefferlab/tiktokscraper",  # Link to your GitHub repo
    packages=find_packages(),        # Automatically find subpackages
    install_requires=[
    "requests",               # For HTTP requests
    "selenium",               # Selenium for web automation
    "chromedriver-autoinstaller",  # Automatically installs the appropriate ChromeDriver
],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
