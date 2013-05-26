#!/usr/bin/python

import sys
import linecache
import random
import os
from lemmatizer import lemmatize_file
import shutil
import time

def load_texts(fname):
    """Reads a texts from a utf-8 CSV file 'fname' in the follwing format: 'text\n'
    """
    reader = open(fname, "r")
    texts = {}
    for i, line in enumerate(reader):
        text = line.strip()
        if not texts.has_key(i):
            texts[i] = text
        else:
            print "Duplicate text id:", i
    #print len(texts), "texts loaded"
    reader.close()

    #for i, t in enumerate(texts):
    #   if i < 30:
    #       print "==%s==%s==%s==" % (i, t, texts[t])

    return texts

def cat_files(input1_fpath, input2_fpath, output_fpath, prefix_line = "", postfix_line = ""):
    output_file = open(output_fpath, "w")
    if(prefix_line != ""):
        output_file.write(prefix_line + "\n")
    
    input1_file = open(input1_fpath, "r")
    output_file.write(input1_file.read())
    input1_file.close()
    
    input2_file = open(input2_fpath, "r")
    output_file.write(input2_file.read())
    input2_file.close()
    
    if(postfix_line != ""):
        output_file.write(postfix_line)    
    output_file.close()
                
#####################################
# Entry point
#####################################
def main(args):

    #Process parameters
    PARAM_NUM = 3 
    if len(sys.argv) < PARAM_NUM + 1:
        print "This script creates a training dataset from a set of positive and negative texts"
        print "Expected", PARAM_NUM, "parameters but was", str(len(sys.argv)-1)
        print "Usage:", sys.argv[0], "<input-positive> <input-negative> <output-dataset>"
        print "<input-positive>\t\tAn input CSV file with one text per line (positive training examples)"
        print "<input-negative>\t\tAn output CSV file with one text per line (negative training examples)"
        print "<output-dataset>\t\tAn output file with the training dataset in XML format."
        sys.exit()

    # Read the command line arguments
    positive_fpath = sys.argv[1]
    negative_fpath = sys.argv[2]
    output_fpath = sys.argv[3] 
    
    # Lemmatize positive and negative texts
    lemmatize_file(positive_fpath, output_fpath + ".positive.xml", True, True)
    lemmatize_file(negative_fpath, output_fpath + ".negative.xml", True, False)

    # Cat xml files 
    cat_files(output_fpath + ".positive.xml", output_fpath + ".negative.xml", output_fpath, "<texts>", "</texts>")

    # Remove temporary files
    os.remove(output_fpath + ".positive.xml")
    os.remove(output_fpath + ".negative.xml")
    
    print "Script has finished successfully."

if __name__ == '__main__':
    main(sys.argv)
