"""xml_transformer.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import parser

def xml_to_graphviz( xml ):
    pass


def xml_to_stoich_matrix( xml ):
    pass

def test( filename ):
    xml = parser.parse_plain_text( filename )
    print( xml_to_stoich_matrix(xml) )

if __name__ == '__main__':
    test( './examples/modela.chem' )
