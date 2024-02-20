from lxml import etree

# Load the XML report and XSLT stylesheet
xml_file = 'test-reports/test_report.xml'  # Path to your XML report
xslt_file = 'xunit.xsl'  # Path to the downloaded XSLT stylesheet

# Parse the XML and XSLT files
xml_doc = etree.parse(xml_file)
xslt_doc = etree.parse(xslt_file)

# Create a transformation
transform = etree.XSLT(xslt_doc)

# Apply the transformation to the XML document
result_tree = transform(xml_doc)

# Save the transformed HTML report to a file
with open('test-reports/test_report.html', 'wb') as html_report:
    html_report.write(etree.tostring(result_tree, pretty_print=True))
