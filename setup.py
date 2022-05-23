from setuptools import find_packages, setup

VERSION = "0.0.1"
DESCRIPTION = "A wrapper for Hypixel's Skyblock API"
LONG_DESCRIPTION = "Makes it much easier to use the Skyblock API from python."

# Setting up
setup(
    name="skypy",
    version=VERSION,
    author="Aditya Rao",
    author_email="araoudupi@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv",
        "colorama",
        "nbt",
    ],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'
    keywords=["python", "first package"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
