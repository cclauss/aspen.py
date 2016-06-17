"""
Define parser/validators for configuration system

Each of these is guaranteed to be passed a unicode object as read from the
environment or the kwargs.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import codecs
import re

from ..simplates.renderers import RENDERERS


# Define a charset name filter.
# =============================
# "The character set names may be up to 40 characters taken from the
#  printable characters of US-ASCII."
#  (http://www.iana.org/assignments/character-sets)
#
# We're going to be slightly more restrictive. Instead of allowing all
# printable characters, which include whitespace and newlines, we're going to
# only allow punctuation that is actually in use in the current IANA list.

charset_re = re.compile("^[A-Za-z0-9:_()+.-]{1,40}$")


def identity(value):
    return value

def media_type(media_type):
    # XXX for now. Read a spec
    return media_type.encode('US-ASCII')

def codec(value):
    codecs.lookup(value)
    return value

def charset(value):
    if charset_re.match(value) is None:
        raise ValueError("charset not to spec")
    return value

def yes_no(s):
    s = s.lower()
    if s in [u'yes', u'true', u'1']:
        return True
    if s in [u'no', u'false', u'0']:
        return False
    raise ValueError("must be either yes/true/1 or no/false/0")

def list_(value):
    # populate out with a single copy of each non-empty item, preserving order
    out = []
    for v in value.split(','):
        v = v.strip()
        if v and not v in out:
            out.append(v)
    return out

def renderer(value):
    if value not in RENDERERS:
        msg = "not one of {%s}" % (','.join(RENDERERS))
        raise ValueError(msg)
    return value.encode('US-ASCII')
