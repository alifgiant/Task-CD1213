# Read File
file = open('6146.xml')

# Paste File
new_file = open ('result.xml', 'w')
new_file.write(file.read())
