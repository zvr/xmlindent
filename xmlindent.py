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
import re
import shutil
import sys
import warnings

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
    # tree.write(fname, encoding='unicode', xml_declaration=False, short_empty_elements=True)
    blocks = pretty(root, 0)
    ser = fmt(blocks)
    with open(fname, 'w') as f:
        f.write(ser)

def pretty(node, level):
    ser = ''
    tag = node.tag
    text = singlespaceline(node.text)
    tail = singlespaceline(node.tail)
    print("\t\t", level, tag, text, tail, node.attrib)
    start_tag = "<" + tag
    if node.attrib:
        for a in ATTRS_SEQ[tag]:
            if a in node.attrib:
                start_tag += ' {}="{}"'.format(a, node.attrib[a])
                del node.attrib[a]
        if node.attrib:
            warning('more attrs remaining in {}: {}'.format(tag, node.attrib.keys()))
    start_tag += ">"
    end_tag = "</" + tag + ">"
    if node.tag in TAGS_block:
        child_level = level + 1
        before = '{0}{1}#{2}{0}{3}#'.format(NL, level, start_tag, child_level)
        after = '{0}{1}#{2}{0}'.format(NL, level, end_tag)
        # before = NL + level + start_tag + NL + child_level
        # after = NL + level + end_tag + NL
    elif node.tag in TAGS_inline:
        child_level = level
        before = start_tag
        after = '{1}{0}{2}#'.format(NL, end_tag, level)
        # before = start_tag
        # after = end_tag + NL + level
    else:
        warning('Tag "{}" neither block nor inline!'.format(tag))
        child_level = level
        before = start_tag
        after = end_tag
    ser += before
    if text:
        ser += text
    for child in node:
        ser += pretty(child, child_level)
    if tail:
        ser += tail
    ser += after
    ser = ser.replace('\n\n', '\n')
    return ser

def fmt(blocks):
    bregexp = re.compile(r'((?P<level>\d+)#)?(?P<paragraph>.*)')
    ser = ''
    for line in blocks.split('\n'):
        if line == '':
            continue
        m = bregexp.match(line)
        if m.group('level'):
            l = int(m.group('level'))
        else:
            warning('Block without level: "{}"'.format(line))
        par = m.group('paragraph')
        if par == '':
            continue
        indent = l * INDENT
        width = LINE_LENGTH - indent
        ser += indent * ' ' + par + '\n'
    return ser


def singlespaceline(txt):
    if txt:
        txt = txt.strip()
        txt = re.sub(r'\s+', ' ', txt)
    return txt


def backup(fname):
    bak_fname = fname + BACKUP_EXT
    shutil.copy(fname, bak_fname)

def warning(msg, category=None):
    warnings.warn(msg, category)

def info(s):
    print(s)

process(sys.argv[1])

