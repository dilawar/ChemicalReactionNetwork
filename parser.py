"""parser.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import lxml.etree as ET
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

def _parse_species( s ):
    m = re.match( r'(\d*)(\w+)', s)
    n = 1
    if m.group(1):
        n = int(m.group(1))
    return str(n), m.group(2)

def _add_sub_prd( r, subXML, prdXML ):
    global root_
    subs, prds = [ _split_line(x, '+') for x in _split_line(r, u'<->') ]

    # Add them to root_
    species = root_.find( 'listOfSpecies' )
    for s in subs + prds:
        # if already exists then do not add them.
        n, name = _parse_species( s )
        if species.xpath( "./species[@name='%s']" % name ):
            print( 'Already added: %s' % name)
        ET.SubElement( species, 'species', compartment='default', id=name, name=name)

    for s in subs:
        n, name = _parse_species( s )
        e = ET.SubElement( subXML, 'speciesReference', species=name, stoichiometry=n)
    for p in prds:
        n, name = _parse_species( p )
        e = ET.SubElement( prdXML, 'speciesReference', species=name, stoichiometry=n)

def _add_reac( line, xml):
    line = re.sub( r'r\d+\:\s*', '', line )
    tx = ET.SubElement( xml, 'raw_input' )
    tx.text = line
    fs = _split_line( line )
    r, params = fs[0], fs[1:]
    params = [ x.split( '=') for x in params ]

    ex = ET.SubElement( xml, 'kineticLaw' )
    ex = ET.SubElement( ex, 'kf_kb_law', attrib=dict(params) )

    # now add substrate and products
    subXML = ET.SubElement( xml, 'listOfReactants' )
    subPrd = ET.SubElement( xml, 'listOfProducts' )
    _add_sub_prd( r, subXML, subPrd )

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
        rid = re.search( r'(r\w+):', line).group(1)
        r = ET.SubElement( xml, 'reaction', id=rid )
        _add_reac( line, r )
    elif line[0].lower() == 'e':
        e = ET.SubElement( xml, 'expr', attrib=dict(lineno=str(idx)) )
        _add_expr( line, e )
    else:
        print( "[WARN ] Unsupported type %s" % line[0] )

def parse_plain_text( text ):
    global root_
    reacs = ET.SubElement( root_, 'listOfReactions' )
    species = ET.SubElement( root_, 'listOfSpecies' )
    for i, l in enumerate(text.split( '\n' )):
        _parse_line( reacs, i, l.strip() )
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
