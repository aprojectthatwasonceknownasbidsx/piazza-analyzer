# Piazza Analyzer

Analyzes data from Piazza through sentiment analysis and keyword checking 

This requires a database from [Piazza-Scraper](https://github.com/bidsX/piazza-scraper).

# Installation

Create a conda environment using

	conda create --name ENV_NAME python=3.4

Install from the list of requirements.


	pip install -r requirements.txt

# How to Run

To run the visualization, do the following. We assume that you have already started your conda environment using

	source activate ENV_NAME

1) If the database hasn't already been created (e.g. this is the first time you are runening the scraper), run the scraper, and copy the database over to this directory.
		
	python -i analyze.py

	>>> analysis = PiazzaAnalyzer()
	>>> analysis.analyze_posts()





# Development

The project structure is as following

- analyze.py- Main Analysis Module
- models.py - Models for SQLAlchemy ORM
- utils.py  - Helpful utilities for parsing Piazza blocks
- rake.py   - Python3 Implementation of  Rapid Automatic Keyword Extraction - Ported from [RAKE](https://github.com/aneesha/RAKE)

