from setuptools import setup, find_packages

setup(
    name="unit",           # How the package is named in pip (e.g., pip install your_package_name)
    version="0.1.0",                    # Your current release version
    description="Parse and store commonly used units", 
    author="GW",
    packages=find_packages(),           # Automatically finds folders with an __init__.py
    install_requires=[                  # Dependencies pip will automatically install
        "numpy",
        "astropy"
    ],
    python_requires=">=3.8",            # Minimum Python version required
)
