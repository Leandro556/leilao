from tika import parser

raw = parser.from_file('/Users/leandrobertocchi/Desktop/slides_05.pdf')

raw['content']