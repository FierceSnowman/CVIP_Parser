from PyPDF2 import PdfReader 
import re
import argparse
"""
A script to parse two types of NCMEC CVIP Reports
"""
__author__ = "Jake Toulomelis"
__date__ = 20240124
__description__ = "A script to parse two types of NCMEC CVIP reports"

parser = argparse.ArgumentParser(description=__description__, epilog="Developed by {} on {}.".format(__author__, __date__))

parser.add_argument("-v", "--version", help="Displays script version information", action="version", version=str(__date__))

parser.add_argument("INPUT_FILE", help="Path to the input file")
parser.add_argument("OUTPUT_FILE", help="Path to the output file")

args = parser.parse_args()

input_file = args.INPUT_FILE
output_file = args.OUTPUT_FILE

reader = PdfReader(input_file) 
print('Stand by. Determining function to use...')

def myfunct1(reader):
    hashlist = set()
    for page in reader.pages:
        text = page.extract_text()

        hashes = re.findall('[0-9a-zA-Z]{32}\.', text)
        for x in hashes:
            hashlist.add(x.strip("."))
    return hashlist

def myfunct2(reader):
    hashlist = set()
    for page in reader.pages:
        text = page.extract_text()
        hashes = re.findall('[/0-9a-zA-Z]{34}\.', text)
        for x in hashes:
            hashlist.add(x.replace("/", "").strip("."))
    return hashlist

result = myfunct1(reader)
if len(result) == 0:
   result = myfunct2(reader)
   if len(result) == 0:
    print('No MD5 values detected in ths report')

with open(output_file, 'a') as f:
    for r in result:
       f.write(str(r + "\n"))

print(*result, sep = "\n")
print(f'result: {type(result)}')
print(f'result: {len(result)} hashes written to file MD5.txt')