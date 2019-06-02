#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the checkMagazine function below.
def checkMagazine(magazine, note):
	note_dict = {}
	for m in magazine:
		try:
			note_dict[m] += 1
		except KeyError:
			note_dict[m] = 1
	print(note_dict)

	for n in note:
		try:
			note_dict[n] -= 1
		except KeyError:
			print('No')
			return

	for k in note_dict:
		if note_dict[k] < 0:
			print('No')
			return
	print('Yes')

if __name__ == '__main__':
	magazine = 'two times three is not four'.split()
	note = 'two times two is four'.split()
	#magazine = 'give me one grand today night'.split()
	#note = 'give one grand today'.split()
	checkMagazine(magazine, note)

