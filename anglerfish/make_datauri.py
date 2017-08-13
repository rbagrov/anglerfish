#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Data URI base64 helper string class, designed for HTML/CSS/JS and images."""


import os
import re
import textwrap

from base64 import urlsafe_b64decode, urlsafe_b64encode
from collections import namedtuple
from mimetypes import guess_type
from pathlib import Path
from shutil import which
from subprocess import run
from tempfile import NamedTemporaryFile
from urllib.parse import quote_plus, unquote_plus
from urllib.request import urlretrieve


__all__ = ("img2webp", "DataURI")


_MIMETYPE_REGEX, _CHARSET_REGEX = r'[\w]+\/[\w\-\+\.]+', r'[\w\-\+\.]+'
_MIMETYPE_RE = re.compile('^{0}$'.format(_MIMETYPE_REGEX))
_DATA_URI_REGEX = (
    r'data:' +
    r'(?P<mimetype>{0})?'.format(_MIMETYPE_REGEX) +
    r'(?:\;charset\=(?P<charset>{0}))?'.format(_CHARSET_REGEX) +
    r'(?P<base64>\;base64)?' +
    r',(?P<data>.*)')
_DATA_URI_RE = re.compile(r'^{0}$'.format(_DATA_URI_REGEX), re.DOTALL)


def img2webp(image_path: str, webp_path: str=None, preset: str="text",
             cwebp: str=which("cwebp"), timeout: int=60) -> str:
    """Try to convert Image to WEBP for max performance."""
    imagepath = Path(image_path)
    if not cwebp or imagepath.suffix not in (".png", ".jpeg", ".jpg", ".tiff"):
        return imagepath  # CWEBP is not installed, return the same image.
    if preset not in "default photo picture drawing icon text":
        preset = "text"  # Text Preset is still Ok,looks like JPG,but tiny.
    webppath = Path(webp_path) if webp_path else imagepath.with_suffix(".webp")
    command = f"{ cwebp } -preset { preset } { imagepath } -o { webppath }"
    return imagepath if run(
        command, shell=True, timeout=timeout).returncode else webppath


class DataURI(str):

    """Data URI Base64 string, designed for Images, WebP autoconversion."""

    @classmethod
    def make(cls, mimetype: str, base64: bool, data: str) -> str:
        """Make a new Data URI Base64 string from arguments."""
        parts = ['data:']
        if mimetype is not None:
            if not _MIMETYPE_RE.match(mimetype):
                raise ValueError(f"Invalid MIME: {mimetype}, {base64}, {cls}.")
            parts.append(mimetype + ';charset=utf-8')
        if base64:
            parts.append(';base64')
            encoded_data = urlsafe_b64encode(data).decode("utf-8")
        else:
            encoded_data = quote_plus(data)
        parts.extend([',', encoded_data])
        return cls(''.join(parts))

    @classmethod
    def from_file(cls, filename: str,
                  base64: bool=True, webp: bool=True) -> str:
        """Make a new Data URI Base64 string from a file."""
        filename = Path(filename)
        if webp and filename.suffix in (".png", ".jpeg", ".jpg", ".tiff"):
            filename = img2webp(filename)
        return cls.make(guess_type(filename.suffix, strict=False)[0],
                        base64, filename.read_bytes())

    @classmethod
    def from_url(cls, url: str, base64: bool=True, webp: bool=True) -> str:
        """Make a new Data URI Base64 string from a remote HTTP URL."""
        _temp = NamedTemporaryFile(suffix=os.path.basename(url)).name
        return cls.from_file(urlretrieve(url, _temp)[0],
                             base64=base64, webp=webp)

    def __new__(cls, *args, **kwargs) -> str:
        """Make a new Data URI Base64 string from arguments."""
        uri = super(DataURI, cls).__new__(cls, *args, **kwargs)
        uri._parse  # Trigger any ValueErrors on instantiation.
        return uri

    def __repr__(self):
        """Represent as string the Data URI Base64."""
        return f"DataURI({ super(DataURI, self).__repr__() })"

    def wrap(self, width: int=80, newline: str="\n") -> str:
        """Wrap Data URI Base64 string based on arguments using textwrap."""
        return type(self)(newline.join(textwrap.wrap(self, int(width))))

    @property
    def mimetype(self) -> str:
        """Return the file MIME Type of the Data URI Base64 string."""
        return self._parse.mimetype

    @property
    def charset(self) -> str:
        """Return the file Encoding of the Data URI Base64 string. UTF-8."""
        return "utf-8"

    @property
    def is_base64(self) -> bool:
        """Return True if its Base64."""
        return self._parse.is_base64

    @property
    def data(self) -> str:
        """Return the raw Binary Data of the Data URI Base64 string."""
        return self._parse.data

    @property
    def _parse(self) -> namedtuple:
        """Auxiliary property method for attributes and parsing."""
        match = _DATA_URI_RE.match(self)
        if not match:
            raise ValueError("Invalid or malformed Data URI: {self!r} {self}.")
        mimetype = match.group('mimetype') or None
        if match.group('base64'):
            data = urlsafe_b64decode(match.group('data').encode("utf-8"))
        else:
            data = unquote_plus(match.group('data'))
        return namedtuple('DataURI', 'mimetype is_base64 data')(
            mimetype, bool(match.group('base64')), data)
