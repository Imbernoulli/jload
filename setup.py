# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jload",
    version="0.2.0", # Incremented version for the new feature/fix
    author="Bohan Lyu", # Replace with your name
    author_email="lyubh22@gmail.com", # Replace with your email
    description="A simple utility to load a list of dictionaries from JSON or JSONL files, with auto-detection of format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Imbernoulli/jload", # Replace with your GitHub repo URL if you have one
    packages=find_packages(where=".", include=['jload', 'jload.*']), # Ensure jload package is found
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
    ],
    python_requires='>=3.7', # json.loads behavior with top-level non-objects is consistent.
    project_urls={
        'Bug Reports': 'https://github.com/Imbernoulli/jload/issues', # Optional
        'Source': 'https://github.com/Imbernoulli/jload/', # Optional
    },
)
