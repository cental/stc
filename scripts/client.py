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

# Main function 

def main():
	# Set the parameters 
	if len(sys.argv) < MIN_ARG_NUM:
		print USAGE
		sys.exit()
	
	positives_fname = sys.argv[1]
	negatives_fname = sys.argv[2]
	icop_query(positives_fname, negatives_fname, get=False)

# Functions

def icop_query(positives_fname, negatives_fname, get=True):
	print "positives:", positives_fname
	print "negatives:", negatives_fname
	
	files = { "negatives" : open(negatives_fname,"r"), "positives" : open(positives_fname,"r") }
	params = { "model":"-1", "name":"model from a service " + time.ctime() }
	if get:
		content = requests.get(ENDPOINT, params=params)
	else:
		content = requests.post(ENDPOINT, params=params, files=files)
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
