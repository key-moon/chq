from setuptools import setup

setup(
    name="chq-cli",
    version="0.0.1",
    install_requires=[],
    extras_require={
    },
    entry_points={
        "console_scripts": [
            "chq = chq.main:main",
        ]
    }
)
