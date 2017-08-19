#!/usr/bin/env python3
#
# quick-n-dirty formatter for SPDX licenses in XML format
#
# Copyright © 2017 Alexios Zavras
# SPDX-License-Identifier: MIT
#

#-----------------------------------------------------------------
# configuration parameters, self-explanatory :-)

INDENT = 2
LINE_LENGTH = 80
BACKUP_EXT = '.backup'

# which tags are inline and which appear on their own lines
TAGS_inline = [
        'alt',
        'b',
        'br',
        'copyright',
        'url',

    ]
TAGS_block = [
        'body',
        'header',
        'li',
        'license',
        'list',
        'notes',
        'optional',
        'p',
        'SPDX',
        'title',
        'urls',

    ]

# attributes for tags, in the order we want them to appear
ATTRS_SEQ = {
        'SPDX': [
            'name',
            'identifier',
            'osi-approved',
            'prettyprinted',
        ],
        'alt': [
            'name',
            'match',
        ],
    }

#-----------------------------------------------------------------

import xml.etree.ElementTree as et
import datetime
import shutil
import sys

NL = '\n'

def process(fname):
    backup(fname)
    tree = et.parse(fname)

    root = tree.getroot()
    if root.tag == 'spdx':
        root.tag = 'SPDX'
        info('changing root element to SPDX (capital letters)')
    ts = '{:%Y%m%d%H%M%S%z}'.format(datetime.datetime.now())
    root.set('prettyprinted', ts)
    # pretty(root, "")
    tree.write(fname,
            encoding='unicode', xml_declaration=False,
            short_empty_elements=True)

def pretty(node, indent):
    ser = ''
    tag = node.tag
    text = singlespaceline(node.text)
    tail = singlespaceline(node.tail)
    debug(len(indent), tag, text, tail, node.attrib)
    start_tag = "<" + tag
    if node.attrib:
        for a in ATTRS_SEQ:
            pass
    start_tag += ">"
    end_tag = "</" + tag + ">"
    if node.tag in TAGS_block:
        child_indent = indent + " " * INDENT
        before = NL + indent + start_tag + NL + child_indent
        after = NL + indent + end_tag + NL
    elif node.tag in TAGS_inline:
        child_indent = indent
        before = start_tag
        after = end_tag + NL + indent
    else:
        warning('Tag', tag, 'neither block nor inline!')
        child_indent = indent
        before = start_tag
        after = end_tag
    ser += before
    if text:
        ser += text
    for child in node:
        ser += pretty(child, child_indent)
    if tail:
        ser += tail
    ser += after
    ser = ser.replace('\n\n', '\n')
    return ser


def singlespaceline(txt):
    if txt:
        txt = txt.strip()
        txt = re.sub(r'\s+', ' ', txt)
    return txt


def backup(fname):
    bak_fname = fname + BACKUP_EXT
    shutil.copy(fname, bak_fname)


process(sys.argv[1])

