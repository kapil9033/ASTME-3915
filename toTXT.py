import xml.etree.ElementTree as ET
import re

def extract_name_attributes(xml_file, intermediate_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Open the intermediate text file for writing
    with open(intermediate_file, 'w') as f:
        # Iterate over all elements
        for elem in root.iter():
            # Check if the element has a 'name' attribute
            name = elem.get('name')
            if name:
                # Write the name and its value to the text file
                f.write(f"name={name}\n")

def filter_type_two_lines(input_file, filtered_file):
    # Open the input and output files
    with open(input_file, 'r') as infile, open(filtered_file, 'w') as outfile:
        # Define a regex pattern to match type 2 lines
        pattern = re.compile(r'name=.*\)$')
        
        # Iterate over each line in the input file
        for line in infile:
            # Check if the line matches the type 2 pattern
            if pattern.match(line.strip()):
                # Write the matching line to the output file
                outfile.write(line)

def remove_number_lines_and_prefix(filtered_file, final_output_file):
    # Open the filtered and final output files
    with open(filtered_file, 'r') as infile, open(final_output_file, 'w') as outfile:
        # Define a regex pattern to match lines with numbers after "name="
        number_pattern = re.compile(r'name=\d+')

        # Iterate over each line in the filtered file
        for line in infile:
            # Check if the line does not match the number pattern
            if not number_pattern.match(line.strip()):
                # Remove "name=" from the beginning of the line
                cleaned_line = line.replace("name=", "", 1)
                # Write the cleaned line to the final output file
                outfile.write(cleaned_line)

def remove_brackets_and_content(final_output_file, cleaned_output_file):
    # Open the final output and cleaned output files
    with open(final_output_file, 'r') as infile, open(cleaned_output_file, 'w') as outfile:
        # Define a regex pattern to remove content within brackets
        bracket_pattern = re.compile(r'\(.*?\)')

        # Iterate over each line in the final output file
        for line in infile:
            # Remove content within brackets
            cleaned_line = bracket_pattern.sub('', line)
            # Write the cleaned line to the cleaned output file
            outfile.write(cleaned_line)

def remove_rte_lines(cleaned_output_file, final_cleaned_output_file):
    # Open the cleaned output and final cleaned output files
    with open(cleaned_output_file, 'r') as infile, open(final_cleaned_output_file, 'w') as outfile:
        # Iterate over each line in the cleaned output file
        for line in infile:
            # Check if the line does not start with "Rte_Call_" or "Rte_Write_"
            if not line.startswith("Rte_Call_") and not line.startswith("Rte_Write_") and not line.startswith("Rte_Read_"):
                # Write the line to the final cleaned output file
                outfile.write(line)

def add_empty_lines_and_replace(final_cleaned_output_file):
    # Read the content from the final cleaned output file
    with open(final_cleaned_output_file, 'r') as infile:
        content = infile.read()

    # Replace consecutive "Xlock_SetEventStatus" with a single instance
    content = re.sub(r'(Xlock_SetEventStatus\s*){2,}', 'Xlock_SetEventStatus\n', content)

    # Split the content into lines for further processing
    lines = content.splitlines(keepends=True)

    # Open the same file for writing
    with open(final_cleaned_output_file, 'w') as outfile:
        # Iterate over each line
        for line in lines:
            # Check if the line starts with "SWC_Com_"
            if line.startswith("SWC_Com_"):
                # Add two empty lines before the line
                outfile.write("\n\n")
            # Write the line to the file
            outfile.write(line)


# Usage
xml_file = 'SWC_Com.xml'
intermediate_file = 'intermediate.txt'
filtered_file = 'filtered_output.txt'
final_output_file = 'cleaned_output.txt'
cleaned_output_file = 'final_cleaned_output.txt'
final_cleaned_output_file = 'output.txt'

# Step 1: Extract name attributes
extract_name_attributes(xml_file, intermediate_file)

# Step 2: Filter type 2 lines
filter_type_two_lines(intermediate_file, filtered_file)

# Step 3: Remove lines with numbers and "name=" prefix
remove_number_lines_and_prefix(filtered_file, final_output_file)

# Step 4: Remove small brackets and content inside
remove_brackets_and_content(final_output_file, cleaned_output_file)

# Step 5: Remove lines starting with "Rte_Call_" and "Rte_Write_"
remove_rte_lines(cleaned_output_file, final_cleaned_output_file)

# Usage
# Step 6: Add empty lines before lines starting with "SWC_Com_"
add_empty_lines_and_replace(final_cleaned_output_file)

#import xml.etree.ElementTree as ET
#
#def extract_name_attributes(xml_file, txt_file):
#    # Parse the XML file
#    tree = ET.parse(xml_file)
#    root = tree.getroot()
#
#    # Open the text file for writing
#    with open(txt_file, 'w') as f:
#        # Iterate over all elements
#        for elem in root.iter():
#            # Check if the element has a 'name' attribute
#            name = elem.get('name')
#            if name:
#                # Write the name and its value to the text file
#                f.write(f"name={name}\n")
#
## Usage
#xml_file = 'SWC_Com.xml'
#txt_file = 'output.txt'
#extract_name_attributes(xml_file, txt_file)


#import xml.etree.ElementTree as ET
#import re
#
#def extract_name_attributes(xml_file, intermediate_file):
#    # Parse the XML file
#    tree = ET.parse(xml_file)
#    root = tree.getroot()
#
#    # Open the intermediate text file for writing
#    with open(intermediate_file, 'w') as f:
#        # Iterate over all elements
#        for elem in root.iter():
#            # Check if the element has a 'name' attribute
#            name = elem.get('name')
#            if name:
#                # Write the name and its value to the text file
#                f.write(f"name={name}\n")
#
#def filter_type_two_lines(input_file, output_file):
#    # Open the input and output files
#    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
#        # Define a regex pattern to match type 2 lines
#        pattern = re.compile(r'name=.*\)$')
#        
#        # Iterate over each line in the input file
#        for line in infile:
#            # Check if the line matches the type 2 pattern
#            if pattern.match(line.strip()):
#                # Write the matching line to the output file
#                outfile.write(line)
#
## Usage
#xml_file = 'SWC_Com.xml'
#intermediate_file = 'intermediate.txt'
#output_file = 'output.txt'
#
## Step 1: Extract name attributes
#extract_name_attributes(xml_file, intermediate_file)
#
## Step 2: Filter type 2 lines
#filter_type_two_lines(intermediate_file, output_file)