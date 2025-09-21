#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="yuv-tools",
    version="1.0.0",
    author="Shriram M",
    author_email="",
    description="A comprehensive collection of Python tools for analyzing and viewing YUV420 video files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shriram-m/yuv-tools",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        # Core requirements - these are always needed
        "numpy>=1.19.0",
    ],
    extras_require={
        "full": [
            "opencv-python>=4.5.0",
            "matplotlib>=3.3.0",
        ],
        "minimal": [
            "Pillow>=8.0.0",
        ],
        "simple": [
            "matplotlib>=3.3.0",
        ],
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "yuv-analyzer=yuv_analyzer:main",
            "yuv-viewer=yuv_viewer:main",
            "yuv-batch-viewer=yuv_batch_viewer:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="yuv video analysis decoder debugging multimedia",
    project_urls={
        "Bug Reports": "https://github.com/shriram-m/yuv-tools/issues",
        "Source": "https://github.com/shriram-m/yuv-tools",
        "Documentation": "https://github.com/shriram-m/yuv-tools#readme",
    },
)
