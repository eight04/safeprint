#! python3

"""A printer suppressing UnicodeEncodeError."""

import os, re, sys, win_unicode_console.streams

from .version import __version__

def Printer():
	if sys.platform == "win32":
		return WinUnicodePrinter()
	else:
		return BasePrinter()

class BasePrinter:
	"""Create printer"""
	def __init__(self):
		self.listeners = set()
		
	def print(self, *objects, sep=" ", end="\n", file=sys.stdout, flush=False):
		"""Micmic print interface"""
		text = sep.join(map(str, objects))
		
		if file is not sys.stdout:
			__builtins__.print(text, end=end, file=file, flush=flush)
		else:
			self.imp_print(text, end=end)
			
		for callback in self.listeners:
			callback(text)
			
	def imp_print(self, text, end):
		"""Implement"""
		__builtins__.print(text, end=end)
		
	def add_listener(self, callback):
		"""Register callback"""
		self.listeners.add(callback)
		
	def remove_listener(self, callback):
		"""Unregister callback"""
		self.listeners.remove(callback)
		
class EchoPrinter(BasePrinter):
	def imp_print(self, text, end):
		"""Use windows echo"""
		for line in text.split("\n"):
			line = re.sub(r"[\&<>|^]", self.escape, line)
			os.system('echo:' + line)
			
	def escape(self, match):
		"""Return escaped echo str."""
		return "^" + match.group()
		
class TryPrinter(BasePrinter):
	def imp_print(self, text, end):
		"""Catch UnicodeEncodeError"""
		try:
			__builtins__.print(text, end=end)
		except UnicodeEncodeError:
			for i in text:
				try:
					__builtins__.print(i, end="")
				except UnicodeEncodeError:
					__builtins__.print("?", end="")
			__builtins__.print("", end=end)
			
class WinUnicodePrinter(BasePrinter):
	def imp_print(self, text, end):
		"""Use win_unicode_console"""
		print(text, end=end, file=win_unicode_console.streams.stdout_text_transcoded)
		
print = Printer().print

if __name__ == "__main__":
	import timeit, functools
	
	texts = ["Hello World!", "你好世界！", "ハローワールド", "हैलो वर्ल्ड"]
	
	def do_print(printer):
		printer.print(*texts)
		
	results = []
	for printer in (EchoPrinter(), TryPrinter(), WinUnicodePrinter()):
		test = functools.partial(do_print, printer)

		result = timeit.timeit("test()", number=100, setup="from __main__ import test")
		results.append(result)
		
	print(results)
