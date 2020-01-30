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

The will generate
 1. results.csv
 2. PI Chart

Using help to list options.
* `python3 src/dosing.py --h`

```
usage: dosing.py [-h] [--VISCODE VISCODE] [--SVDOSE SVDOSE]
                 [--ECSDSTXT ECSDSTXT] [--path PATH]

A utility to create csv report

optional arguments:
  -h, --help           show this help message and exit
  --VISCODE VISCODE    'VISCODE' set variable to filter report generation.
  --SVDOSE SVDOSE      'SVDOSE' set variable to filter report generation
  --ECSDSTXT ECSDSTXT  'ECSDSTXT' set variable to filter report generation
  --path PATH          'path' set variable to write report to directory

```

If you want to execute with an optional arguments. Issue this on terminal. The list of available choices are not known as the available dataset could be a small sample. Note: `VISCODE`, `path` and `SVDOSE` takes `str` as an argument and `ECSDSTXT` takes `int`. No type casting is however required.

 `python3 src/dosing.py --VISCODE w04`
 `python3 src/dosing.py --ECSDSTXT -4`
 
 Not all are arguments are valid choices and the script will generate exceptions in case frames are not materialized.
 
 # Testing
 * `pytest src/test_dosing.py `
 or
  * `pytest src/test_dosing.py -v` {verbose mode}
 
The test will result in 2 passes and a fail.

  1. First test to sanity check merge and filter logic with valid default properties - `test_valid_action`
  2. Second test to sanity check merge and filter logic by setting arbitary values but valid Dtypes values for `ECSDSTXT` filter produces a frame with size 0 - `test_invalid_action`
  
  3.Inavlid Dtype results in Type Error wehen `ECSDSTXT` is paased a `str` value of 200.
 
 



