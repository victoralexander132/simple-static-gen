import re
from textnode import BlockType

def block_to_block_type(block):
    # Check for heading (1-6 # characters followed by space)
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING
    
    # Check for code block (starts with ``` and newline, ends with ```)
    if block.startswith('```') and block.endswith('```'):
        lines = block.split('\n')
        if len(lines) >= 3 and lines[0] == '```' and lines[-1] == '```':
            return BlockType.CODE
    
    # Check for quote block (every line starts with "> ")
    lines = block.split('\n')
    if all(line.startswith('> ') for line in lines):
        return BlockType.QUOTE
    
    # Check for unordered list (every line starts with "- ")
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list (lines start with "1. ", "2. ", etc.)
    if all(re.match(rf'^{i}\. ', line) for i, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST
    
    # Default to paragraph
    return BlockType.PARAGRAPH