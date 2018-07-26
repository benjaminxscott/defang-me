#!/usr/bin/env python

import re

# https://gist.github.com/dperini/729294
RE_URLS = re.compile(
    r'((?:(?P<protocol>[-.+a-zA-Z0-9]{1,12})://)?'
    r'(?P<auth>[^@\:]+(?:\:[^@]*)?@)?'
    r'((?P<hostname>'
    r'(?!(?:10|127)(?:\.\d{1,3}){3})'
    r'(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})'
    r'(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})'
    r'(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])'
    r'(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}'
    r'(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))'
    r'|'
    r'(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)'
    r'(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*'
    r')(?P<tld>\.(?:[a-z\u00a1-\uffff]{2,}))'
    r'))'
    r'(?::\d{2,5})?'
    r'(?:/\S*)?',
    re.IGNORECASE
)
RE_IP_URLS = re.compile(
    r'((?:(?P<protocol>[-.+a-zA-Z0-9]{1,12})://)?'
    r'(?P<auth>[^@\:]+(?:\:[^@]*)?@)?'
    r'(?P<ip>\d+\.\d+\.\d+\.\d+))'
    r'(?P<path>/\S*)?',
    re.IGNORECASE
)

PROTOCOL_TRANSLATIONS = {
    'http': 'hXXp',
    'https': 'hXXps',
    'ftp': 'fXp',
}


def defang_protocol(proto):
    return PROTOCOL_TRANSLATIONS.get(proto.lower(), '({0})'.format(proto))


def defang_ip(ip):
    head, tail = ip.split('.', 1)
    return '{0}[.]{1}'.format(head, tail)


def defang(line):
    clean_line = line
    for match in RE_URLS.finditer(line):
        clean = ''
        if match.group('protocol'):
            clean = defang_protocol(match.group('protocol'))
            clean += '://'
        if match.group('auth'):
            clean += match.group('auth')
        clean += match.group('hostname')
        clean += match.group('tld').replace('.', '[.]')
        clean_line = clean_line.replace(match.group(1), clean)
    for match in RE_IP_URLS.finditer(line):
        clean = ''
        if match.group('protocol'):
            clean = defang_protocol(match.group('protocol'))
            clean += '://'
        if match.group('auth'):
            clean += match.group('auth')
        clean += defang_ip(match.group('ip'))
        clean_line = clean_line.replace(match.group(1), clean)
    return clean_line


def defanger(infile, outfile):
    for line in infile:
        clean_line = defang(line)
        outfile.write(clean_line)


def refang(line):
    dirty_line = re.sub(r'\((\.|dot)\)', '.',
                        line, flags=re.IGNORECASE)
    dirty_line = re.sub(r'\[(\.|dot)\]', '.',
                        dirty_line, flags=re.IGNORECASE)
    dirty_line = re.sub(r'(\s*)h([x]{1,2})p([s]?)://', r'\1http\3://',
                        dirty_line, flags=re.IGNORECASE)
    dirty_line = re.sub(r'(\s*)(s?)fxp(s?)://', r'\1\2ftp\3://',
                        dirty_line, flags=re.IGNORECASE)
    dirty_line = re.sub(r'(\s*)\(([-.+a-zA-Z0-9]{1,12})\)://', r'\1\2://',
                        dirty_line, flags=re.IGNORECASE)
    return dirty_line


def refanger(infile, outfile):
    for line in infile:
        dirty_line = refang(line)
        outfile.write(dirty_line)
