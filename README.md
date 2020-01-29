# dm-code-challenge
Coding challenge @ UCSD

# Setting up

Create a separate venv for this project

*  `python3 -m venv <venv_name> .`

Install packages listed on requirements.txt

*  `pip install -r requirements.txt`

# Executing

For executing the scripts with the default configurations.
*  `python3 src/dosing.py`

Using help to list options.
* `python3 src/dosing.py --h`

`usage: dosing.py [-h] [--VISCODE VISCODE] [--SVDOSE SVDOSE]
                 [--ECSDSTXT ECSDSTXT] [--path PATH]

A utility to create csv report

optional arguments:
  -h, --help           show this help message and exit
  --VISCODE VISCODE    'VISCODE' set variable to filter report generation.
  --SVDOSE SVDOSE      'SVDOSE' set variable to filter report generation
  --ECSDSTXT ECSDSTXT  'ECSDSTXT' set variable to filter report generation
`



