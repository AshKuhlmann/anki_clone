from setuptools import setup, find_packages

setup(
    name="anki_clone",
    version="0.1.0",
    packages=find_packages(where="anki_clone/src"),
    package_dir={"": "anki_clone/src"},
    install_requires=[
        # Add dependencies here
    ],
    entry_points={
        "console_scripts": [
            # Add command-line interfaces here
        ],
    },
)