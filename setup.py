from setuptools import setup

setup(
    name="datasette-cognee",
    version="0.1.0",
    py_modules=["datasette_cognee"],
    entry_points={
        "datasette": [
            "cognee = datasette_cognee"
        ]
    },
    install_requires=["datasette", "cognee"],
)
