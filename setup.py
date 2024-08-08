from setuptools import setup, find_packages

setup(
    name="masterflow",
    description="Workflow for analysis in master project about unidentified zoonotic virus that could be passed by spillover",
    version="0.0.1",
    author="Yago Dias",
    author_email="yag.dias@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "masterflow = scripts.masterflow.main:main",
        ],
    },
)
