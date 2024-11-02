from setuptools import setup, find_packages

setup(
    name="mcqgenerator",
    version="0.0.1",
    packages=find_packages(),
    author="arun kumar",
    author_email="arunaswin3583@gmail.com",
    install_requires=[
        "langchain",
        "streamlit",
        "python-dotenv",
        "PyPDF2",
    ],
)