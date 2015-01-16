import os
import re

def trimLines( input_lines ):
	output_lines = [];
	for line in input_lines:
		output_lines.append(re.sub("\s\s+" , " ", line))
	return output_lines;
	
	

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
	current_position = 0
	found_position = 0
	found = True
	
	while ((found_position > -1) and (current_position <= len(input_string))):
		found_position = input_string.lower().find(find_string, current_position)
		if (found_position > -1):
			found = True;
			for ignore_string in ignore_strings:
				if (-1 < input_string.lower().find(ignore_string,current_position) <= found_position):
					found = False;
					break
			if found:
				input_string = input_string[:found_position] + new_string + input_string[found_position + (len(find_string)):]
				current_position = found_position + len(new_string) + 1
			else:
				current_position = found_position + 1
	return input_string;
		
	

def customParser( input_strings, find_string, new_string, ignore_strings):
	input_strings = splitLines(input_strings);
	output_lines = splitLines(input_strings);
	first_run = True;
	while ((input_strings != output_lines) or first_run):
		input_strings = list(output_lines);
		first_run = False;
		for index in range(len(output_lines)):
			output_lines[index] = findString(output_lines[index], find_string.lower(), new_string, ignore_strings)			
		input_strings = splitLines(input_strings);
		output_lines = splitLines(output_lines);
	return output_lines;
		

		
def customIndent( input_lines ):
	input_lines = splitLines(input_lines)
	output_lines = []
	indent_counter = 0
	for line in input_lines:
		if line.strip() == "}":
			indent_counter = indent_counter - 1
		elif line.strip() == "};":
			indent_counter = indent_counter - 1
		else:
			for x in ["}forEach*"]:
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
		print("Error End of File Indent Counter is not Zero")
	return output_lines;
		
		
		
files = os.listdir()	
for filename in files:
	if (filename.title().lower().endswith('-new')) is False:
		with open(filename) as f:
			input_lines = f.readlines()
		indent = 0
		output_lines = [];
		f = open(filename + "-new", "w")
		output_lines = trimLines(input_lines);
		output_lines = splitLines(output_lines);
#									#output_lines	 #String to Find,  #Replacement String,  #List of Strings to Ignore);
#		output_lines = customParser(output_lines,    "{",              "\n{\n",              ["{}", "{true}", "{false}"]);	
		output_lines = customParser(output_lines, "{", "\n{\n", ["{}", "{true}", "{false}"]);	
		output_lines = customParser(output_lines, ":{", ":\n{\n", []);
		output_lines = customParser(output_lines, "}", "\n}", [";};", "{}", "}count", "}foreach", "{true}", "{false}"]);
		output_lines = customParser(output_lines, "}", "\n}\n", [";};", "};", "{}", "}count", "}foreach", "{true}", "{false}"]);
		output_lines = customParser(output_lines, "};", "};\n", ["};\n"]);
		output_lines = customParser(output_lines, "else", "\nelse\n", []);
		output_lines = customParser(output_lines, ";", ";\n", ["};"]);
		output_lines = customParser(output_lines, "then{", "then\n{", []);
		output_lines = customIndent(output_lines)
		for line in output_lines:
			f.write(line + "\n")
		f.close()
