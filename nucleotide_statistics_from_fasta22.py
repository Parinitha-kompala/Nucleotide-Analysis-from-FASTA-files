#!/usr/bin/env python3
import argparse
import sys

def get_fh(filename, mode):
   """
   get_fh function will 1) read in file name. 2) open a file and 'read' or 'write'
   Purpose of the function is to open the file name passed in and pass back the file handle.
   * All opening and closing of files in your program should use the get_fh function
   """
   fh = None
   try:
      if comm == 'r':
          fh = open(filename,'r')
      elif comm == 'w':
          fh = open(filename,'w')
      else:
          raise ValueError('Command should be r or w')
   except IOError as e:
      print(e)
   except ValueError as e:
      print(e)
   return fh

def get_header_and_sequence_lists(fh):
   header = []
   sequence = []
   firstline = True

   for line in fh:
      if line[0] == '>':
         if firstline == True:
            firstline = False
         else:
            sequence.append(linestore)
         header.append(line.strip())
         linestore = ""
      else:
         linestore = linestore+line.strip()

   sequence.append(linestore)
   _check_size_of_lists(header, sequence)

   return header, sequence

def _check_size_of_lists(header_list, sequence_list):
    """
    function will read in the header and sequence list (returned from get_header_and_sequence_lists).
    function will initiate sys.exit if the size of the lists passed in are not the same.
    "_" indicates for internal use.
    """
    if len(header_list) != len(sequence_list):
        print("Exit")
        sys.exit(0)
    else:
        return True

def _get_accession(string):
   accession = string.split()
   accession = accession[0]
   accession=accession[1:]
   return accession

def _get_nt_occurrence(letter, string):
   return string.count(letter)
    
       
def main():
   parser = argparse.ArgumentParser()
   parser.add_argument('--infile', dest = 'infile', type = str, help = 'Path to the file to open', required = True)
   parser.add_argument('--outfile', dest = 'outfile', type = str, help = 'Path to the output file', required = True)
   args = parser.parse_args()
   fh_in = get_fh(args.infile, "r")
   header, sequence = get_header_and_sequence_lists(fh_in)
   fh_in.close()

   fh_out = get_fh(args.outfile, "w")
   fh_out.write("Number Accession   A's   G's   C's   T's   N's   Length   GC%\n")


   for i in range(len(header)):
      accession = _get_accession(header[i])
      num_As = _get_nt_occurrence('A', sequence[i])
      num_Gs = _get_nt_occurrence('G', sequence[i])
      num_Cs = _get_nt_occurrence('C', sequence[i])
      num_Ts = _get_nt_occurrence('T', sequence[i])
      num_Ns = _get_nt_occurrence('N', sequence[i])

      gc = (num_Gs + num_Cs)*100/(len(sequence[i]))

      fh_out.write('{:5} {:10} {:5} {:5} {:5} {:5} {:5}   {:5}   {:5.2f}\n'.format(i+1, accession, num_As, num_Gs, num_Cs, num_Ts, num_Ns, len(sequence[i]), gc))

   fh_out.close()

if __name__ == '__main__':
   main()
