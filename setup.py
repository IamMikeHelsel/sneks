from setuptools import setup, find_packages

setup(
    name="sneks",
    version="0.1.0",
    description="A modern Snake game implementation",
    author="Sneks Developer",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "pygame",
    ],
    entry_points={
        "console_scripts": [
            "sneks=main:main",
        ],
    },
)
