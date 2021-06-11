"""
File: pdb_fasta_splitter.py
Help messages will guide user through the basic command/execution of the
Sample command for executing the program:
python3 pdb_fasta_splitter.py --infile ss.txt
"""
import argparse
import sys


def get_fh(filename, mode):
    """"
    @input: filename, mode
    @return: returns file handler
    """
    try:
        if mode == 'r':
            file_handler = open(filename, 'r')
        elif mode == 'w':
            file_handler = open(filename, 'w')
        else:
            raise ValueError('Command should be r or w')
    except FileNotFoundError:
        raise FileNotFoundError
    except IOError:
        raise IOError
    except ValueError:
        raise ValueError
    return file_handler


def get_header_and_sequence_lists(fh_in):
    """
    Take in a list and calculate the statistics
    @inputs: takes the input file handle generated by get_fh function and performs the actions
    @return: returns header list and sequence list
    """
    header_list = list()
    sequence_list = list()
    temp = ""
    for line in fh_in:  # using strip removing new line characters
        line = line.strip()
        if line.startswith(">"):  # if line starts with > it appends to header list
            header_list.append(line)
            if len(temp) != 0:
                sequence_list.append(temp)
                temp = ""
        else:  # if the line doesnt starts with > storing in tempand appends to sequence list
            temp = temp + line

    if len(temp) != 0:
        sequence_list.append(temp)

    _check_size_of_lists(header_list, sequence_list)
    return header_list, sequence_list


def _check_size_of_lists(sequence_header, secstr_header):
    """
    Take in a list and calculate the statistics
    @input : takes input as header of sequence and secondary structure
    @return: sys.exist if the size of both lists are not equal
    """  # if the length of header and sequence doesnt matches it exits

    if len(sequence_header) != len(secstr_header):
        print("The size of the sequences and the header lists is different")
        print("Are you sure the FASTA is in correct format")
        sys.exit()
    else:
        return True


def main():
    """ Business Logic """
    args = get_cli_args()
    file = args.file
    fh_in = get_fh(file, 'r')
    list_headers, list_seqs = get_header_and_sequence_lists(fh_in)
    file1 = get_fh("pdb_protein.fasta", "w")  # writing the file
    file2 = get_fh("pdb_ss.fasta", "w")  # writing the file
    protein_seq = 0
    ss_seq = 0
    count = len(list_headers)
    for i in range(count):
        if "sequence" in list_headers[i]:  # looping over list_headers and seqs to files
            file1.write(str(list_headers[i])+'\n')
            file1.write(str(list_seqs[i])+'\n')
            protein_seq = protein_seq + 1
        else:  # the rest part adds here
            file2.write(str(list_headers[i]) + '\n')
            file2.write(str(list_seqs[i]) + '\n')
            ss_seq = ss_seq + 1
    file1.close()
    file2.close()  # closing the files
    print(f"Found {protein_seq} protein sequences", file=sys.stderr)
    print(f"Found {ss_seq} ss sequences", file=sys.stderr)  # printing the output


def get_cli_args():
    """
     Just get the command line options using argparse
     @return: Instance of argparse arguments
     """
    parser = argparse.ArgumentParser(
        description="Give the fasta sequence file name to do the splitting")
    parser.add_argument('-f', '--infile',
                        dest='file',
                        type=str,
                        help='Path to the file to open',
                        required=True)
    return parser.parse_args()


if __name__ == '__main__':
    main()
