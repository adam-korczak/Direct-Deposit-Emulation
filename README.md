
# Direct-Deposit-Emulation
My response to the direct deposit emulation engineering challenge.

# Setup/Dependencies

Built in Windows with Python 3.12.4. [Python 3.12.4 Stable Release](https://www.python.org/downloads/release/python-3124)
	
If requests library not installed, run 'pip install requests'.
	Libraries:
	 - import requests
	 - import csv
	 - import json
	 
	Run with: 'python main.py'. Afterwards, expects a user input in the format of YYYY-MM-DD.
	 Valid range includes 2024-06-14 to 2024-06-28.

	Delete or move 'processedPayments.csv' before attempting to run main.py and generating a new output.
 
 	Requires bearer token + base url 
	All data seen in example output is mock/test. 

