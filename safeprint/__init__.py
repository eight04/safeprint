#! python3

"""A printer suppressing UnicodeEncodeError."""

from __future__ import print_function

import sys

__version__ = "0.2.0"

PRINT = print
TTY = sys.stdout.isatty()
PY2 = sys.version_info < (3, 0, 0)
PY36 = sys.version_info >= (3, 6, 0)
WIN32 = sys.platform == "win32"

try:
	UNICODE = unicode
except NameError:
	UNICODE = None

def STR(o):
	if UNICODE:
		if isinstance(o, str):
			o = UNICODE(o, "utf-8")
		o = UNICODE(o)
	else:
		o = str(o)
	return o

try:
	import win_unicode_console.streams
	WIN_UNICODE_CONSOLE = True
except ImportError:
	WIN_UNICODE_CONSOLE = False

def wuc_should_be_fixed():
	stdout = getattr(win_unicode_console.streams, "STDOUT", None)
	return not stdout or stdout.should_be_fixed()

def Printer(): # pylint: disable=invalid-name
	if TTY:
		if PY36 or not WIN32:
			return BasePrinter()

		if WIN_UNICODE_CONSOLE and wuc_should_be_fixed():
			return WinUnicodePrinter()

		return TryPrinter()

	if PY2:
		return EncodePrinter()

	return Py3EncodePrinter()

class BasePrinter:
	"""Create printer"""
	def __init__(self):
		self.listeners = set()

	def print(self, *objects, **kwargs):
		"""Micmic print interface"""
		file = kwargs.get("file")

		if file is not None and file is not sys.stdout:
			PRINT(*objects, **kwargs)

		else:
			sep = STR(kwargs.get("sep", " "))
			end = STR(kwargs.get("end", "\n"))

			text = sep.join(STR(o) for o in objects)

			self.imp_print(text, end)

		for callback in self.listeners:
			callback(text)

	def imp_print(self, text, end):
		"""Implement"""
		PRINT(text, end=end)

	def add_listener(self, callback):
		"""Register callback"""
		self.listeners.add(callback)

	def remove_listener(self, callback):
		"""Unregister callback"""
		self.listeners.remove(callback)

class TryPrinter(BasePrinter):
	def imp_print(self, text, end):
		"""Catch UnicodeEncodeError"""
		try:
			PRINT(text, end=end)
		except UnicodeEncodeError:
			for i in text:
				try:
					PRINT(i, end="")
				except UnicodeEncodeError:
					PRINT("?", end="")
			PRINT("", end=end)

class WinUnicodePrinter(BasePrinter):
	def imp_print(self, text, end):
		"""Use win_unicode_console"""
		PRINT(text, end=end, file=win_unicode_console.streams.stdout_text_transcoded)

class EncodePrinter(BasePrinter):
	def imp_print(self, text, end):
		"""Directly send utf8 bytes to stdout"""
		sys.stdout.write((text + end).encode("utf-8"))

class Py3EncodePrinter(BasePrinter):
	def imp_print(self, text, end):
		"""Directly send utf8 bytes to stdout"""
		sys.stdout.buffer.write((text + end).encode("utf-8"))

print = Printer().print
