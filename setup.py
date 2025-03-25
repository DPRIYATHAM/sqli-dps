from setuptools import find_packages, setup

setup(
    name="sqli_dps",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["joblib", "pandas", "scikit-learn", "numpy"],
    include_package_data=True,
    package_data={
        "sqli_dps": [
            "lexer.l",
            "wrapper.c",
            "wrapper.h",
            "train.py",
            "inference.py",
            "model.pkl",
            "sqliv2cleaned.csv",
            "sql_tokenizer.so",
        ],
    },
    author="",
    author_email="your.email@example.com",
    description="A Simple SQL injection detection based on ml",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/DPRIYATHAM/sqli-dps/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
