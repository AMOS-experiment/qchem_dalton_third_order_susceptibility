from sys import argv
import numpy as np
import sympy as sp
import scipy.constants as constants

import parse_gammas


def main():
	gamma_list = parse_gammas.extract_gammas_from_file(argv[1]) 

	print(gamma_list)

if __name__ == "__main__":
	main()