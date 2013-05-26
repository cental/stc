#!/usr/bin/python

import os
import sys
import re
import cPickle
from xml.etree import ElementTree
from urllib import urlencode
import codecs
import time
import requests

# Constants

USAGE = """This script calls icop service and parses the result. 

Usage:\t./%s <positives-file> <negatives-file>
<positives-file>\tFile with the positive training examples.
<negatives-file>\tFile with the negative training examples. 
""" % os.path.basename(sys.argv[0])

MIN_ARG_NUM = 3 # program name + required parameters
ENDPOINT = "http://localhost/train/index.php"
ENDPOINT_PREDICT = "http://localhost/index.php"

# Main function 

def main():
	# Set the parameters 
	if len(sys.argv) < MIN_ARG_NUM:
		print USAGE
		sys.exit()
	
	positives_fname = sys.argv[1]
	negatives_fname = sys.argv[2]

	#if len(sys.argv) > MIN_ARG_NUM:
	#	start_with = int(sys.argv[2])
	#else:
	#	start_with = 0
	
	#train_query(positives_fname, negatives_fname, get=False)
	predict_query(positives_fname, get=False)
	predict_query(negatives_fname, get=False)

# Functions

def load_text(fname):
	n = 50000
	f = open(fname, "r")
	text = ""
	#for i, line in enumerate(f):
	#	if i < n: text = text + "\n" + line
	#	if i % 100 == 0: print i
	text = f.read()
	f.close()
	return text

def predict_query(fname, get=True):
	print "fname:", fname
	filenames = load_text(fname)

	params = { "filename":filenames, "process":"classify", "model":"3" }
	if get:
		content = requests.get(ENDPOINT_PREDICT, params=params)
	else:
		content = requests.post(ENDPOINT_PREDICT, params)
	print content.content

	return content	

def train_query(positives_fname, negatives_fname, get=True):
	print "positives:", positives_fname
	print "negatives:", negatives_fname
	positives = load_text(positives_fname)
	negatives = load_text(negatives_fname)

	params = { "positives":positives, "negatives":negatives,\
			"model":"-1", "name":"model from a service " + time.ctime() }
	if get:
		content = requests.get(ENDPOINT, params=params)
	else:
		content = requests.post(ENDPOINT, params)
	print content.content

	return content	


def query_xml(params):
	resp, content = query(params)
	return content

def query_struct(params):
	response, content = query(params)
	if response["status"] == "200":
		return parse_response(content)
	else:
		return [], []

def parse_response(xml_response):
	""" Parses the xml result and returns the following structure:
	(<documents>, <skills>)
	<documents> ::= [<document>, <document>, ...]
	<document> ::= (id, name, score)
	<skills> ::= [<skill>, <skill>, ...]
	<skill ::= (id, name, score)
	"""
	docs = []
	skills = []
	e = ElementTree.XML(xml_response)
	if e.tag == "results":
		for atype in e.findall(".//document"):
			if "id" in atype.attrib:
				doc_id = atype.get("id") 
			else: 
				continue

			if "name" in atype.attrib:
				name = atype.get("name") 
			else: 
				continue

			if "score" in atype.attrib:
				score = atype.get("score") 
			else: 
				continue

			docs.append((doc_id, name, score))
		
		for atype in e.findall(".//skill"):
			if "id" in atype.attrib:
				skill_id = atype.get("id") 
			else: 
				continue

			if "name" in atype.attrib:
				name = atype.get("name") 
			else: 
				continue

			if "score" in atype.attrib:
				score = atype.get("score") 
			else: 
				continue

			skills.append((skill_id, name, score))

	elif e.tag == "error":
		for atype in e.findall('message'):
			print "Error:",  atype.text
	else:
		print "Error: unknown result format"

	return docs, skills


def query(params):
	url = ENDPOINT + "ws?" + urlencode(params)
	#print "query:", url
	h = httplib2.Http()
	resp, content = h.request(url, "GET")
	#print content
	return resp, content	


if __name__ == '__main__':
	main()
