"""
File: pdb_fasta_splitter.py

The program reads the file containing both the sequence and secondary
seperates both the headers and sequences into seperate list
 and gives the count of the sequences and secondary structure in each file
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
    for line in fh_in:
        line = line.strip()
        if line.startswith(">"):
            header_list.append(line)
            if len(temp) != 0:
                sequence_list.append(temp)
                temp = ""
        else:
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
    """
    if len(sequence_header) != len(secstr_header):
        sys.exit("The size of the sequences and the header lists is different\n"
                 +"Are you sure the FASTA is in correct format")
    else:
        return True


def _get_accession(string):
    """"
    @input : Takes sting as an input
    @return: returns string
    """
    accession = string.split()
    accession = accession[0]
    accession = accession[1:]
    return accession


def _get_nt_occurrence(letter, string):
    """
    @param letter:
    @param string:
    @return:
    """
    if letter in ('A', 'G', 'T', 'C', 'N'):
        return string.count(letter)
    sys.exit("Did not code this condition")


def print_sequence_stats(fh_out, header, sequence):
    """
    @param fh_out:
    @param header:
    @param sequence:
    @return:
    """
    count = len(header)
    for i in range(count):
        accession = _get_accession(header[i])
        a_count = _get_nt_occurrence('A', sequence[i])
        g_count = _get_nt_occurrence('G', sequence[i])
        c_count = _get_nt_occurrence('C', sequence[i])
        t_count = _get_nt_occurrence('T', sequence[i])
        n_count = _get_nt_occurrence('N', sequence[i])

        gc_count = (g_count + c_count) * 100 / (len(sequence[i]))
        data = '{:5} {:10} {:5} {:5} {:5} {:5} {:5}   {:5}   {:5.2f}\n'
        fh_out.write(
            data.format(i + 1, accession, a_count, g_count, c_count, t_count,
                        n_count, len(sequence[i]), gc_count))
    return [a_count, g_count, c_count, t_count, n_count, len(sequence[i]), gc_count]


def main():
    """ Business Logic """
    args = get_cli_args()
    fh_in = get_fh(args.infile, 'r')
    list_headers, list_seqs = get_header_and_sequence_lists(fh_in)
    fh_out = get_fh(args.outfile, "w")
    fh_out.write("Number Accession   A's   G's   C's   T's   N's   Length   GC%\n")

    print_sequence_stats(fh_out, list_headers, list_seqs)


def get_cli_args():
    """
     Just get the command line options using argparse
     @return: Instance of argparse arguments
     """
    parser = argparse.ArgumentParser(
                description="Give the fasta sequence file name to do the splitting")
    parser.add_argument('--infile',
                        dest='infile',
                        type=str,
                        help='Path to the file to open',
                        required=True)
    parser.add_argument('--outfile',
                        dest='outfile',
                        type=str,
                        help='Path to the file to open',
                        required=True)

    return parser.parse_args()


if __name__ == '__main__':
    main()