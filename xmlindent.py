#!/usr/bin/env python3
#
# quick-n-dirty formatter for SPDX licenses in XML format
#
# Copyright © 2017 Alexios Zavras
# SPDX-License-Identifier: MIT
#

#-----------------------------------------------------------------
# configuration parameters, self-explanatory :-)
# they are simply defaults; can be overwritten by command-line options

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

VERSION = '1.0'

import argparse
import datetime
import re
import shutil
import sys
import warnings
import xml.etree.ElementTree as et

NL = '\n'

def process(fname):
    backup(fname)
    tree = et.parse(fname)

    root = tree.getroot()
    if root.tag == 'spdx':
        root.tag = 'SPDX'
        warning('changing root element to SPDX (capital letters)')
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
    # print("\t\t", level, tag, text, tail, node.attrib)
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
        for fmtline in to_lines(par, width):
            ser += indent * ' ' + fmtline + '\n'
    return ser


def to_lines(text, width):
    words = text.split()
    count = len(words)
    last_offset = 0
    offsets = [last_offset]
    for w in words:
        last_offset += len(w)
        offsets.append(last_offset)

    cost = [0] + [10 ** 20] * count
    breaks = [0] + [0]      * count
    for i in range(count):
        j = i + 1
        while j <= count:
            w = offsets[j] - offsets[i] + j - i - 1
            if w > width:
                break
            penalty = cost[i] + (width - w) ** 2
            if penalty < cost[j]:
                cost[j] = penalty
                breaks[j] = i
            j += 1
    lines = []
    last = count
    while last > 0:
        first = breaks[last]
        lines.append(' '.join(words[first:last]))
        last = first
    lines.reverse()
    return lines


def singlespaceline(txt):
    if txt:
        txt = txt.strip()
        txt = re.sub(r'\s+', ' ', txt)
    return txt


def backup(fname):
    if config['backup_ext']:
        bak_fname = fname + config['backup_ext']
        shutil.copy(fname, bak_fname)


def warning(msg, category=None):
    warnings.warn(msg, category)

#-----------------------------------------------------------------
# main program

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='Indent XML file(s)')
    parser.add_argument('filename', nargs='+',
            help='the XML files to process')
    parser.add_argument('-w', '--width', action='store', type=int,
            default = LINE_LENGTH,
            help='the maximum width of the lines in output')
    parser.add_argument('-i', '--indent', action='store', type=int,
            default = INDENT,
            help='the number of spaces each level is indented')
    parser.add_argument('-b', '--backup', action='store',
            default = BACKUP_EXT,
            help='the backup extension')
    parser.add_argument('-B', '--nobackup', action='store_true',
            help='do not keep a backup of the input file(s)')
    parser.add_argument('--inline-tags', action='store',
            help='space-separated list of tags to be rendered inline')
    parser.add_argument('--block-tags', action='store',
            help='space-separated list of tags to be rendered as blocks')
    parser.add_argument('-V', '--version', action='version',
            version='%(prog)s ' + VERSION,
            help='print the program version')

    args = parser.parse_args()

    config = dict()
    config['inline'] = TAGS_inline
    config['block'] = TAGS_block
    config['max_width'] = args.width
    config['lvl_indent'] = args.indent
    config['backup_ext'] = args.backup
    if args.nobackup:
        config['backup_ext'] = None
    if args.inline_tags:
        config['inline_tags'] = args.inline_tags.split()
    if args.block_tags:
        config['block_tags'] = args.block_tags.split()

    for fname in args.filename:
        process(fname)

