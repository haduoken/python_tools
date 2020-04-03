import xml.etree.ElementTree as et

et_test_xml = et.parse('test.xml')
print(et_test_xml)
root = et_test_xml.getroot()
print(root)
