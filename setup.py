#!/usr/bin/env python3
"""
Setup script for OdooProtect (PyPI: odooprotect)
"""

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="odooprotect",
    version="1.0.0",
    author="OdooProtect Team",
    author_email="support@creativedev.co.id",
    description="Advanced Odoo Protect Python code obfuscator with machine ID binding",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dynaz/odooprotect",
    license="MIT",
    py_modules=["odooprotect"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: Software Development :: Build Tools",
    ],
    python_requires=">=3.6",
    keywords="obfuscation security protection python code",
    project_urls={
        "Bug Reports": "https://github.com/dynaz/odooprotect/issues",
        "Source": "https://github.com/dynaz/odooprotect",
        "Documentation": "https://odooprotect.readthedocs.io/",
    },
    entry_points={
        "console_scripts": [
            "odooprotect=odooprotect:main",
        ],
    },
)
