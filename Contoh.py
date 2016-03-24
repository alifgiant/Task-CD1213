__author__ = 'maakbar'

import xml.etree.ElementTree as ET

if __name__ == "__main__":
    tree = ET.parse('6146.xml')
    root = tree.getroot()
    
