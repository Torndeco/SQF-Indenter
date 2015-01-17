# RULES		
#FIND STRING + LIST OF STRINGS TO IGNORE use Regrex https://docs.python.org/3.4/library/re.html

rules = [		
#FIND STRING    #REPLACE STRING        #LIST OF STRINGS TO IGNORE
["{",           "\n{\n",               ["{\s*}", "{\s*True\s*}", "{\s*False\s*}"]],
[":\s*{",          ":\n{\n",              []],
["}",           "\n}",                 [";\s*}\s*;", "{\s*}", "}\s*Count", "}\s*Foreach", "{\s*True\s*}", "{\s*False\s*}"]],
["}",           "}\n",                 [";\s*}\s*;", "}\s*;", "{\s*}", "}\s*Count", "}\s*Foreach", "{\s*True\s*}", "{\s*False\s*}"]],
["}\s*;",          "};\n",                ["}\s*;\n"]],
["else",        "\nelse\n",            []],
[";",           ";\n",                 ["}\s*;"]],
["then\s*{",       "then\n{",             []]]


## Coming Soon ability to define Rules for Indentation.........


## Don't edit Below this unless you know what you are doing


import os
import re

def prepareLines( input_lines ):
	
	output_line = "";
	for line in input_lines:
		output_line = output_line + line;

	output_line = (re.sub("\s\s+" , " ", output_line.strip()))

	return [output_line];
	

def splitLines( input_lines ):
	temp_lines = [];
	output_lines = [];
	for line in input_lines:
		temp_lines = temp_lines + line.split("\n");
		
	for line in temp_lines:
		if len(line.strip()) > 0:
			output_lines.append(line)
	return output_lines;
	
	
	
def findString (input_string, find_string, new_string, ignore_strings):

	re_search = 0
	current_position = 0

	regrex = re.compile(find_string, re.IGNORECASE)
	while ((re_search != None) and (current_position < len(input_string))):
		re_search = regrex.search(input_string, current_position)
		if re_search != None:
			found = True
			for ignore_string in ignore_strings:
				regrex_ignore = re.compile(ignore_string, re.IGNORECASE)
				re_ignore_search = regrex_ignore.search(input_string, current_position)
				if re_ignore_search != None:
					if re_ignore_search.start() <= re_search.start():
						found = False
						break
			if found:
				input_string = input_string[:re_search.start()] + new_string + input_string[re_search.end():]
				current_position = re_search.start() + (len(new_string) + 1)
			else:
				current_position = re_search.start() + 1
		else:
			break
	return input_string;

	

def customParser(input_strings, find_string, new_string, ignore_strings):
	input_strings = splitLines(input_strings);
	output_lines = splitLines(input_strings);
	first_run = True;
	while ((input_strings != output_lines) or first_run):
		input_strings = list(output_lines);
		first_run = False;
		for index in range(len(output_lines)):
			output_lines[index] = findString(output_lines[index].strip(), find_string.lower(), new_string, ignore_strings)			
		input_strings = splitLines(input_strings);
		output_lines = splitLines(output_lines);
	return output_lines;
		

		
def customIndent(filename, input_lines ):
	input_lines = splitLines(input_lines)
	output_lines = []
	indent_counter = 0
	for line in input_lines:
		if line.strip() == "}":
			indent_counter = indent_counter - 1
		elif line.strip() == "};":
			indent_counter = indent_counter - 1
		else:
			for x in ["}\s*forEach*", "}\s*count*"]:
				if re.search(x, line.strip(), re.IGNORECASE) != None:
					indent_counter = indent_counter - 1

		for x in range(0, indent_counter):
			line = "\t" + line
		output_lines.append(line)
		if line.strip() == "{":
			indent_counter = indent_counter + 1
		else:
			for x in []:
				if re.search(x, line.strip(), re.IGNORECASE) != None:
					indent_counter = indent_counter + 1
			for x in []:
				if re.search(x, line.strip(), re.IGNORECASE) != None:
					indent_counter = indent_counter - 1
					
	if indent_counter != 0:
		print("Error Indent Counter is not Zero at end of file: " + filename)
	return output_lines;
		
		
		
files = os.listdir()	
for filename in files:
	if (filename.title().lower().endswith('-new')) is False:
		print("File: " + filename)	
		with open(filename) as f:
			input_lines = f.readlines()
		indent = 0
		output_lines = [];
		f = open(filename + "-new", "w")
		output_lines = prepareLines(input_lines);
		output_lines = splitLines(output_lines);
		
		for rule in rules:
			print("WORKING.... Rule...." + str(rule))
			output_lines = customParser(output_lines, rule[0], rule[1], rule[2])
		output_lines = customIndent(filename, output_lines)
		output_lines = customIndent(filename, output_lines)
		
		for line in output_lines:
			f.write(line + "\n")
		f.close()