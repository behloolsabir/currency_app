# Currency Exchange App
 [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Travis Status](https://img.shields.io/travis/behloolsabir/currency_app)

## What is this?
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
python currency.py -s usd
```

To get buy values for USD
```sh
python currency.py -b usd
```
## Output
---
Output is saved in `data` of parent of working directory. 
