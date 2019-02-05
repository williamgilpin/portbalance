import os, glob
import numpy as np

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

key_location = os.path.join(ROOT_DIR, 'assets', 'keys.txt')
if len(glob.glob(key_location))>0:
	_API_KEY = str(np.loadtxt(key_location, dtype='str'))
	_API_FLAG = "tiingo"
else:
	_API_FLAG = "rh"
	warnings.warn("""Tiingo API key not found, falling back to robinhood API. To fix, 
		sign up for an API key at the Tiingo website, then store it in a file named
		 "keys.txt" located in the resources directory""")