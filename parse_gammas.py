from sys import argv
import numpy as np
"""
take a dalton output file like output_files/NB_rotated_static_gamma_STO-3G_hf.out and extract the
gamma info
"""

def strip_gamma(k):
    return k.replace("gamma(", "").replace(")", "")


def convert(k):
    """convert "Y;Y,Z,Z" to (1,1,2,2)
    output is a tuple
    """
    convert_axes = {
        "X": 0,
        "Y": 1,
        "Z": 2
    }
    k = k.replace(";", ",")
    parts = k.split(',')
    converted = [convert_axes[part] for part in parts]
    return tuple(converted)


def parse_gamma(gammas):
    """convert gamma output list from 
    extract_gammas_from_file(filename)
    the following list format:
    A 3x3x3 list with indeces,
    J, K (0 for X, 1 for Y and 2 for Z) and for third dim, index 0 => gammaJJKK, index 1 => gamma JKJK and index 2 => gamma JKKJ
    """
    gamma_list = np.zeros(3,3,3)
    for gamma_line in gammas:
        _, k, v = gamma_line.split()
        k = convert(strip_gamma(k))
        v = float(v)
        if(k[0] == k[1] and k[1] == k[2] and k[2] == k[3]):
            gamma_list[k[0]][k[0]][0] = v
            gamma_list[k[0]][k[0]][1] = v
            gamma_list[k[0]][k[0]][2] = v
        elif (k[0] == k[1] and k[2] == k[3]):
            gamma_list[k[0]][k[2]][0] = v
        elif (k[0] == k[2] and k[1] == k[3]):
            gamma_list[k[0]][k[1]][1] = v
        elif (k[0] == k[3] and k[1] == k[2]):
            gamma_list[k[0]][k[1]][2] = v
        print(k)
        print(v)
    return gamma_list


def extract_gammas_from_file(filename):
    with open(filename) as f:
        lines = f.readlines()
        gammas = []
        for line in lines:
            if "@ gamma(" in line:
                gammas.append(line)
        gammas = parse_gamma(gammas)
        return gammas

if __name__ == "__main__":
    gamma_output = extract_gammas_from_file(argv[1])
    print(gamma_output)