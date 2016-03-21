# Piazza Analyzer

Analyzes data from Piazza through velocity and keyword checking through a 
visual interface

This requires a database from [Piazza-Scraper](https://github.com/bidsX/piazza-scraper).

# Installation

Create a conda environment using

	conda create --name ENV_NAME python=3.4

Install from the list of requirements.


	pip install -r requirements.txt

# How to Run

To run the visualization, do the following. We assume that you have already started your conda environment using

	source activate ENV_NAME

1) If the database hasn't already been created (e.g. this is the first time you are running the scraper), run the scraper, and copy the database over to this directory.
	
2) First, we must run the Natural Language Analysis on the database:
	
	python -i analyze.py

	analysis = PiazzaAnalyzer()
	analysis.analyze_posts()

2) Once the analyzer has finished, to run the visualization, run the server and load the webpage: localhost:5000

	python -i server.py



# Screenshots

![Post Analysis](/screenshots/singlepost.png?raw=true "Post Analysis")

![Histogram](/screenshots/histogram.png?raw=true "Histogram")

![Table View](/screenshots/table.png?raw=true "Table View")

# Development

The project structure is as following

- models.py - Models for SQLAlchemy ORM
- utils.py  - Helpful utilities for parsing Piazza blocks
- server.py - The main Flask Application
- static/ 	- All HTML/CSS/JS files
- rake.py   - Python3 Implementation of  Rapid Automatic Keyword Extraction - Ported from [RAKE](https://github.com/aneesha/RAKE)

