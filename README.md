# FunBlocks Checker

### Checking termination and confluence of FunBlocks program
FunBlocks checker is a verification tool allowing to check termination and confluence of a [FunBlocks](https://github.com/kyouko-taiga/FunBlocks) program using a simple command line interface. 

## Requirements

* [pip](https://pypi.org/project/pip/) for Python 3
* Ubuntu 18.04


## Installation
* Clone the repository and move to the root of the project
* To allow script execution, run:
```
chmod +x CLI/callMaude.sh
```
* To use the command line interface, run:
```
pip install .
```
* You can now use the command of the FunBlocks checker tool.

## Usage 
### FunBlocks checker allows the following commands:

```
funblocks_checker init FILENAME
```

Generate the Maude file from a FunBlocks program. FILENAME is the full path of the corresponding FunBlocks file 

```
funblocks_checker [--log] (ct | check_termination)
```

Check  termination  of  the  current  FunBlocks  file  (generated  with  the init command).  We can use ```ct``` or ```check_termination```. The flag ```--log``` is optional, use it to display in the browser a description of the proof.

```
funblocks_checker (cf | check_confluence)
```

Check confluence of the current FunBlocks file (generated with the ```init``` command). We can use ```cf``` or ```check_confluence```.
