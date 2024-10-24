## Illumio coding assessment - Urmil Parikh

# Basics:
* Used python 3.9 for development, not tested with lower versions.
* The code files are in `src` dir. The data files are in `data` dir.
* The program can accept input for csv file for lookup table and log file for actual data
* 2 output files are generated: `tag_counts.out` and `combo_counts.out`
* The program can run for default as well as custom flow log file. For custom flow log file pass additional param of column index for dstport and protocol number.
* Assumption: Log file has to be a SSV (space separated value) file.
* Assumption: Tags are alphanumeric and not just a number.
* Assumption: Protocol number is valid. A dictionary is created from the csv file downloaded from https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml. That dict is used for protocol keyword lookup from the protocol number.
* To test for big code size I wrote a simple python script to create a mock log and csv file.

# Implementation
* The main function accepts input and reads the log and csv files.
* It loops through each log file line to extract `dstport` and `protocol`.
* The input file is read using python's line read feature in order to load whole the file in memory.
* The protocol is converted to keyword using protocol number to keyword map.
* Create a new LogProcessor class object which has function to accept data and update counts accordingly.
* The dstport and protocol info is passed to the function call for LogProcessor which has a hashmap to store key: a tuple between dstport and protocol. It updates the count as it encounters each combinations.
* Also lookup and update count for tags for each combination.
* Finally print the counts in output files.

# Steps to run
* To run the program run `python3 src/main.py` with additional params.
* Run `python3 src/main.py -h` for more info on how to pass the params.
* It takes 2 required inputs passed as flags: logfile path passed as `--logfile` and csvfile path passed as `--csvfile`
* To pass custom flow log file, an additional param `--custom` must be passed with a space separated column index for `dstport` and `protocol`.

# Testing Done
* Tested with `small.csv` and `small.log` for smaller dataset.
* Run `python3 test_log_generator.py` and `python3 test_csv_generator.py` in the `data` dir to generate `big.log` and `big.csv` for testing.
* Pass the big files as imput to test the code for stress testing of hude data size.
* Also tested for a small custom flow log file.


