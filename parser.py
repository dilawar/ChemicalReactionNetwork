"""parser.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

try:
    import lxml.etree as ET
except Exception as e:
    import xml.etree.ElementTree as ET
import os
import sys
import re

root_ = ET.Element( 'root' )

def _add_comment( xml, idx, line):
    e = ET.SubElement( xml, 'comment', attrib=dict(lineno=str(idx)) )
    e.text = line

def _split_line( line, at=','):
    fs = [ x.strip() for x in line.split( at ) if x.strip() ]
    return fs

def _add_reac( line, xml):
    line = re.sub( r'r\d+\:\s*', '', line )
    tx = ET.SubElement( xml, 'raw_input' )
    tx.text = line
    fs = _split_line( line )
    r, params = fs[0], fs[1:]
    params = [ x.split( '=') for x in params ]
    for k, v in params:
        x = ET.SubElement( xml, 'param', name = k, value=v )

def _add_expr( line, xml ):
    line = re.sub( r'e\S*\:\s*', '', line )
    tx = ET.SubElement( xml, 'raw_input' )
    tx.text = line
    fs = _split_line( line, '=' )
    lhs, rhs = fs[0], fs[1]
    e = ET.SubElement( xml, 'LHS', dict(var=re.sub(r'\(\s*\w+\s*\)', '', lhs)) )
    e.text = lhs
    e = ET.SubElement( xml, 'RHS' )
    e.text = rhs

def _parse_line( xml, idx, line ):
    if not line:
        return
    if line[0] == '#':
        _add_comment( xml, idx, line)
        return 
    
    if line[0].lower() == 'r':
        r = ET.SubElement( xml, 'reaction', attrib=dict(lineno=str(idx)) )
        _add_reac( line, r )
    elif line[0].lower() == 'e':
        e = ET.SubElement( xml, 'expr', attrib=dict(lineno=str(idx)) )
        _add_expr( line, e )
    else:
        print( "[WARN ] Unsupported type %s" % line[0] )

def parse_plain_text( text ):
    global root_
    for i, l in enumerate(text.split( '\n' )):
        _parse_line( root_, i, l.strip() )
    return root_

def parse( filename, fmt = 'plain' ):
    # Parse given filename 
    with open( filename, 'r' ) as f:
        txt = f.read()
    if fmt == 'plain':
        return parse_plain_text( txt )
    else:
        print( "[WARN ] Format %s is not supported" % fmt )

if __name__ == '__main__':
    xml = parse( './examples/modela.chem' )
    xmlDoc = ET.tostring( xml, pretty_print = True )
    try:
        xmlDoc = xmlDoc.decode('utf8')
    except Exception as e:
        pass
    print( xmlDoc )
