import argparse
#Adding command line parse arguments. This will likely be replaced b y the gui, but for running the scripts it lets you pass stuff in when you call it
parser = argparse.ArgumentParser(description='Search for terms in the OCLC file.')
req = parser.add_argument_group('Required arguments')
req.add_argument("-p", "--path", help="Path to OCLC xml.", required=True)
req.add_argument("-i", "--input", help="File of terms to search for. Separate unique terms by newlines, and other spellings of the same term by commas",required=True)
req.add_argument("-t", "--tolerance", help="Tolerance for how many words can separate words in the sentence",type=int,default=0,required=False)
req = parser.parse_args()
#other imports
import xml.etree.ElementTree as ET
from alive_progress import alive_bar
#import logging
import re
#Alive bar gives it a progroess bar which is really cool, the number there is the number of times bar() will be called in the code
with alive_bar(58265) as bar:
	with open(req.path) as f:
		i = 0
		#Get the list of terms you need
		inp = open(req.input).readlines()
		#Create files for each term
		for line in inp:
			with open("./reqout/" + re.sub("\n","",line.split(",")[0]), "w") as init:
				init.write("id\tyear\tlang\ttitle\n")
				init.close()
		#For each line in the set of marc21 data
		for line in f:
			#Incrementor for bar, only doing it every 100 cycles because having it once per cycle slows the code down a lot cause its called so many times per second
			i = i+1
			if i%100 == 0:
				bar()
			#GO through XML data
			root = ET.fromstring(line)
			for child in root:
				#Get values from specific tags
				if child.attrib.get('tag') == '001':
					code = child.text
				if child.attrib.get('tag') == '008':
					year = child.text[7:11]
					lang = child.text[35:38]
				if child.attrib.get('tag') == '245':
					for val in child:
						if val.attrib.get('code') == 'a':
							#Check titles for the keywords
							for l in inp:
								found = False
								for term in l.split(","):
									term = re.sub("\n","",term)
									#Do some nonsense to check how many words separate key words, if multiple keywords needed
									if len(term.split(" ")) > 1:
										splt = term.split(" ")
										spot = 0
										ind = 999
										for word in val.text.lower().split(" "):
											try:
												if word.index(splt[spot]) == 0:
													if val.text.lower().split(" ").index(word) - ind <= req.tolerance+1:
														ind = val.text.lower().split(" ").index(word)
														spot = spot+1
														#If good, save to a file
														if spot == len(splt):
															print("ding")
															with open("./reqout/" + re.sub("\n","",l.split(",")[0]), "a") as appen:
																out = code + "\t" + year + "\t" + lang + "\t" + val.text + "\n"
																appen.write(out)
																found = True
																appen.close()
													else:
														ind = -999
											except:
												print("",end="")
									#Otherwise, just check if the words are inside the title

									else:
										for word in val.text.lower().split(" "):
											try:
												#If so, save to a file
												if word.index(re.sub("\n","",term.lower())) == 0 and not found:
													with open("./reqout/" + re.sub("\n","",l.split(",")[0]), "a") as appen:
														out = code + "\t" + year + "\t" + lang + "\t" + val.text + "\n"
														appen.write(out)
														found = True
														appen.close()
											except:
												print("",end="")





