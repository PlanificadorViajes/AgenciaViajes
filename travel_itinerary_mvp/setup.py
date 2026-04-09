"""Setup configuration for Travel Itinerary MVP System."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="travel-itinerary-mvp",
    version="1.0.0",
    author="Travel Itinerary MVP Team",
    author_email="contact@travel-itinerary-mvp.com",
    description="Sistema de generación iterativa de itinerarios de viaje usando arquitectura basada en agentes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/travel_itinerary_mvp",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=[
        "python-dateutil>=2.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "isort>=5.10.0",
            "pre-commit>=2.20.0",
            "bandit>=1.7.0",
            "safety>=2.0.0",
        ],
        "llm": [
            "openai>=1.0.0",
            "anthropic>=0.3.0",
        ],
        "validation": [
            "pydantic>=2.0.0",
        ],
        "cli": [
            "click>=8.0.0",
            "rich>=13.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "travel-itinerary=travel_itinerary_mvp.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "travel_itinerary_mvp": [
            "config/prompts/*.txt",
        ],
    },
    zip_safe=False,
    keywords=[
        "travel",
        "itinerary",
        "agent-based",
        "planning",
        "ai",
        "mvp",
        "generator",
        "critic",
    ],
)
