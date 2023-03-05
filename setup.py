from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    long_description = file.read()
setup(
    name='dispie',
    version='0.0.11',
    author = "Pranoy Majumdar",
    author_email = "officialpranoy2@gmail.com",
    description = "🚀 A fantastic library created for use with Discord.py",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url="https://github.com/PranoyMajumdar/dispie",
    project_urls = {
        "Homepage": "https://github.com/PranoyMajumdar/dispie"
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages = find_packages(),
    python_requires = ">=3.7",
    license="MIT"
)