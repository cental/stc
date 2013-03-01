#!/usr/bin/python

import sys
import linecache
import random
import os
from lemmatizer import lemmatize_file
import shutil


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
                
def split_csv_texts(input_fpath, output1_fpath, output2_fpath, split_percent):
    # Check the parameters 
    if (not os.path.exists(input_fpath)) or (split_percent < 0) or (split_percent > 1):
        print "Error: wrong input arguments."
        return
    	
    # Open the files
    input_file = open(input_fpath, "r")
    output1_file = open(output1_fpath,"w", buffering=1)
    output2_file = open(output2_fpath,"w", buffering=1)
    
    # Get a random sample of line numbers
    input_texts = load_texts(input_fpath)
    boundary = int(len(input_texts) * split_percent)
    input_lines = range(0, len(input_texts) - 1)
    output1_lines = random.sample(input_lines, boundary)
    output1_lines = dict(zip(output1_lines[0::2], output1_lines[1::2]))
    print input_fpath, ":", len(input_texts), "texts"
    print output1_fpath, ":", boundary, "texts"
    print output2_fpath, ":", len(input_texts) - boundary, "texts"    
    
    # Save the lines in two separate files
    for line in input_lines:
        if line in output1_lines:
            output1_file.write(input_texts[line] + "\n") #linecache.getline(input_fpath, line))
        else:
            output2_file.write(input_texts[line] + "\n") #linecache.getline(input_fpath, line))
    
    linecache.clearcache()    
    input_file.close()
    output1_file.close()
    output2_file.close()

#####################################
# Entry point
#####################################
def main(args):

    #Process parameters
    PARAM_NUM = 3 
    if len(sys.argv) < PARAM_NUM + 1:
        print "This script creates train and test datasets from a set of positive and negative texts samples"
        print "Expected", PARAM_NUM, "parameters but was", str(len(sys.argv)-1)
        print "Usage:", sys.argv[0], "<input-positive-texts> <input-negative-texts> <output-test> <output-train> [<split-fraction>]"
        print "<input-positive>\t\tAn input CSV file with one text per line (positive training examples)"
        print "<input-negative>\t\tAn output CSV file with one text per line (negative training examples)"
        print "<output-dir>\t\tAn output directory with a dataset ready to train."
        print "<split-fraction>\tPercent of texts in the <output-test> (in (0;1), default 0.9 => 10/90)"
        sys.exit()

    # Read the command line arguments
    positive_fpath = sys.argv[1]
    negative_fpath = sys.argv[2]
    output_fpath = sys.argv[3] 
    test_fpath = output_fpath + "/train.xml"
    train_fpath = output_fpath + "/valid.xml"
    if len(sys.argv) > PARAM_NUM + 1:
        SPLIT_PERCENT = float(sys.argv[PARAM_NUM + 1])
    else:
        SPLIT_PERCENT = 0.9

    # Initialize the directory
    if not os.path.exists(output_fpath):
        os.mkdir(output_fpath)
    shutil.copy2('./../data/test/stopos.csv', output_fpath + '/stopos.csv')
    shutil.copy2('./../data/test/stopwords.csv', output_fpath + '/stopwords.csv')
    shutil.copy2('./../data/test/relations.csv', output_fpath + '/relations.csv')
    
    # Split positive and negative texts
    split_csv_texts(positive_fpath, output_fpath + "/positive.train.csv", output_fpath + "/positive.test.csv", SPLIT_PERCENT)
    split_csv_texts(negative_fpath, output_fpath + "/negative.train.csv", output_fpath + "/negative.test.csv", SPLIT_PERCENT)

    # Lemmatize positive and negative texts
    lemmatize_file(output_fpath + "/positive.test.csv", output_fpath + "/positive.test.xml", True, True)
    lemmatize_file(output_fpath + "/positive.train.csv", output_fpath + "/positive.train.xml", True, True)
    lemmatize_file(output_fpath + "/negative.test.csv", output_fpath + "/negative.test.xml", True, False)
    lemmatize_file(output_fpath + "/negative.train.csv", output_fpath + "/negative.train.xml", True, False)

    # Cat test files 
    cat_files(output_fpath + "/positive.test.xml", output_fpath + "/negative.test.xml", test_fpath, "<texts>", "</texts>")
    cat_files(output_fpath + "/positive.train.xml", output_fpath + "/negative.train.xml", train_fpath, "<texts>", "</texts>")    

    # Remove temporary files
    os.remove(output_fpath + "/positive.test.csv")
    os.remove(output_fpath + "/positive.train.csv")
    os.remove(output_fpath + "/negative.test.csv")
    os.remove(output_fpath + "/negative.train.csv")
    os.remove(output_fpath + "/positive.test.xml")
    os.remove(output_fpath + "/positive.train.xml")
    os.remove(output_fpath + "/negative.test.xml")
    os.remove(output_fpath + "/negative.train.xml")
    
    print "Script has finished successfully."

if __name__ == '__main__':
    sys.exit(main(sys.argv))
