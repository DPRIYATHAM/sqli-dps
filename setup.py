import os
import subprocess

from setuptools import Extension, find_packages, setup
from setuptools.command.build import build

name = "sqlidps"  # Updated project/package name


class CustomBuild(build):
    def run(self):
        # Define paths for our files
        lex_file = os.path.join(name, "lexer.l")
        lex_c = os.path.join(name, "lex.yy.c")
        wrapper_c = os.path.join(name, "wrapper.c")
        target = os.path.join(name, "sql_tokenizer.so")
        lex_o = os.path.join(name, "lex.yy.o")
        wrapper_o = os.path.join(name, "wrapper.o")

        # Retrieve python configuration flags
        python_includes = (
            subprocess.check_output(["python3-config", "--includes"])
            .decode()
            .strip()
            .split()
        )
        python_ldflags = (
            subprocess.check_output(["python3-config", "--ldflags"])
            .decode()
            .strip()
            .split()
        )

        # If lex.yy.c does not exist, generate it using flex
        if not os.path.exists(lex_c):
            print("Generating lex.yy.c from lexer.l ...")
            subprocess.check_call(["flex", "-o", lex_c, lex_file])

        # Compile lex.yy.c to lex.yy.o with the appropriate flags
        print(f"Compiling {lex_c} to {lex_o} ...")
        subprocess.check_call(
            ["gcc", "-fPIC", "-Wall", "-O2", "-c", lex_c, "-o", lex_o] + python_includes
        )

        # Compile wrapper.c to wrapper.o with the same flags
        print(f"Compiling {wrapper_c} to {wrapper_o} ...")
        subprocess.check_call(
            ["gcc", "-fPIC", "-Wall", "-O2", "-c", wrapper_c, "-o", wrapper_o]
            + python_includes
        )

        # Link object files to create the shared module
        print(f"Linking {lex_o} and {wrapper_o} into {target} ...")
        subprocess.check_call(
            [
                "gcc",
                "-bundle",
                "-undefined",
                "dynamic_lookup",
                lex_o,
                wrapper_o,
                "-o",
                target,
            ]
            + python_ldflags
        )

        # Continue with the standard build process
        super().run()


setup(
    name="sqlidps",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["joblib", "scikit-learn", "numpy", "pandas"],
    include_package_data=True,
    package_data={
        "sqlidps": [
            "lexer.l",
            "wrapper.c",
            "wrapper.h",
            "model.pkl",
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
    cmdclass={"build": CustomBuild},
)
