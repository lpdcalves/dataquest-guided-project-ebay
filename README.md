# Guided Project: Exploring eBay Car Sales Data

This repo contains an implementation of Dataquest's [Exploring eBay Car Sales](https://app.dataquest.io/c/54/m/294/guided-project%3A-exploring-ebay-car-sales-data/) Data Guided Project.

This project was initially developed in a jupyter notebook, and then transformed into a python script, both of which are stored here. The main goal of this project was to practice the use of clean code technologies, such as pylint, on top of datascience applications.

## Technologies Used

A few of the most notorious and widespread tools for datascience and code cleaning were utilized, such as:
- Jupyter
- Pandas
- Pylint

## Code Cleanliness

Pylint was used to validate the cleanliness of the code, achieving a score of 10/10.

To run pylint simply install it using pip:
```
pip install pylint
```
And then run our file through it:
```
pylint carsales.py
```
If your code is up to [PEP8](https://www.python.org/dev/peps/pep-0008/) standards, your pylint output should look similar to this:
```
-------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 8.36/10, +1.64)
```