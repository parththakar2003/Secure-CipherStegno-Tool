"""
Setup configuration for Secure CipherStegno Tool
"""

from setuptools import setup, find_packages
import sys
import os

# Check Python version before attempting installation
if sys.version_info < (3, 8):
    sys.stderr.write(
        "=" * 70 + "\n"
        "ERROR: Python 3.8 or higher is required\n"
        "=" * 70 + "\n"
        "Current Python version: {0}.{1}.{2}\n".format(
            sys.version_info.major,
            sys.version_info.minor,
            sys.version_info.micro
        ) +
        "Required Python version: 3.8 or higher\n\n"
        "This tool requires Python 3.8+ because:\n"
        "  • Pillow >= 10.0.0 requires Python 3.8+\n"
        "  • NumPy >= 1.24.0 requires Python 3.8+\n"
        "  • FastAPI >= 0.104.0 requires Python 3.8+\n"
        "  • Other dependencies require modern Python versions\n\n"
        "Please upgrade to Python 3.8 or higher:\n"
        "  https://www.python.org/downloads/\n"
        "=" * 70 + "\n"
    )
    sys.exit(1)

# Read README for long description
def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

# Read requirements
def read_requirements(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='secure-cipherstegno-tool',
    version='3.1.0',
    author='Parth Thakar',
    author_email='parththakar2003@users.noreply.github.com',
    description='Advanced cryptography and steganography toolkit for secure communication',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/parththakar2003/Secure-CipherStegno-Tool',
    project_urls={
        'Bug Reports': 'https://github.com/parththakar2003/Secure-CipherStegno-Tool/issues',
        'Source': 'https://github.com/parththakar2003/Secure-CipherStegno-Tool',
        'Documentation': 'https://github.com/parththakar2003/Secure-CipherStegno-Tool/blob/main/docs/USAGE.md',
    },
    packages=find_packages(exclude=['tests*', 'examples*']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Multimedia :: Sound/Audio',
    ],
    keywords='cryptography steganography security encryption aes rsa caesar cipher privacy',
    python_requires='>=3.8',
    install_requires=read_requirements('requirements.txt'),
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
        ],
        'docs': [
            'sphinx>=5.0.0',
            'sphinx-rtd-theme>=1.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'cipherstegno=cli:main',
            'cipherstegno-gui=app:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    license='MIT',
)
