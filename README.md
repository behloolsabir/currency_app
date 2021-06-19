# Currency Exchange App
 [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Travis Status](https://img.shields.io/travis/behloolsabir/currency_app)

## What is this?
--- 
This is a Python app. It sources the currency rates from multiple sources and gives the best sell or buy options for all the valid currencies for the base currency. 

### Supported Sources
---
  - fawazahmed0:
    - https://github.com/fawazahmed0/currency-api
  - frankfurter:
    - https://www.frankfurter.app/docs/

## How To Use This? 
---
Python version 3.9.4<br>
Refer to the [requirements.txt](src/requirements.txt) for the dependencies. 

Sample:<br>
To get sell values for USD
```sh
python -m src.main -s usd
```

To get buy values for USD
```sh
python -m src.main -b usd
```
To get both buy and sale values for USD
```sh
python -m src.main -sb usd
```
### Unit Test 
---
To run unit test run: 
```sh
pytest
```

## Output
---
Output is saved in `data` of parent of working directory. 

## Design Comments
---
* Design is flexible to add new providers in future. 
  * Add a new child class to provider base class to add a new provider. 
* Output is provided in a model class named `trade` so that any future changes to output ways can be handled gracefully. 