# Python Successor Finder
**Enter an obsolete material to receive a successor.**

## Dependencies
- Python 3.10 (https://www.python.org/downloads/release/python-3100/)
- pyinstaller (https://pyinstaller.org/en/stable/)
- ttkthemes (https://ttkthemes.readthedocs.io/en/latest/)
- numpy (https://numpy.org/)

## Definitions
**Direct Successor** - A product specifically listed as the successor for an obsolete product. (e.g. If the successor is to be selected from a general series such as the Power Panel C-Series, it is NOT a direct successor.) DOES NOT have to be a 1:1 replacement.

## Installing Release Build
1. Download .zip file to desired location and extract
2. *(Optional) Right click executable and select Send to -> Desktop to create a desktop shortcut*

## Installing Source Using PyInstaller
### Installing Dependency Libraries
|Library        | Installation Command      |
|---------------|---------------------------|
|pyinstaller    | pip install -U pyinstaller|
|tkkthemes      | pip install ttkthemes     |
|numpy          | pip install numpy         |


### Installation Process
While in main directory, open a terminal and enter 

`pyinstaller 'BnR SPF.spec'`


## How to Edit the Database
https://sqlitebrowser.org/

## Regex Cheat Sheet
- `^` Start of line/string
- `\.` escape input to use "."
- `.` matches any character (except for line terminators)
- `*` matches the previous token between zero and unlimited times
- `+` matches the previous token between one and unlimited times
- `{x}` matches the previous token x number of times
- `\d` matches any digit (0-9)
 
 
