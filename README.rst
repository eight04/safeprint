safeprint
=========

A printer suppressing UnicodeEncodeError.

Install
-------

::

	pip install safeprint
	
	
Usage
-----

Basic:

::

	from safeprint import print
	
	print("你好世界！" "こんにちは世界" "안녕하세요세계")

Hook callback:
	
::

	import safeprint
	
	printer = safeprint.Printer()
	
	def callback(text):
		# do something with the text
	
	printer.add_listener(callback)
	
	printer.print(1, 2, 3, sep=", ")

	
Dependencies
------------

* win-unicode-console - required if python version < 3.6.

Dev-dependencies
----------------

* bumpr
* wheel
* docutils
* twine
* setuptools

Performance note
----------------

* BasePrinter - Use ``builtins.print``. Python has builtin unicode support after Python 3.6.0.
* EchoPrinter - Call ``echo`` command to print unicode chars. Extreme slow.
* TryPrinter - Print each chars separately and print a "?" for invalid char.
* WinUnicodePrinter - Use win-unicode-console module.

Changelog
---------

* 0.1.2 (Jul 21, 2016)

  - Compatible with win-unicode-console 0.5

* 0.1.1 (Apr 15, 2016)

  - Fix builtins bug.

* 0.1.0 (Apr 15, 2016)

  - Initial release.
	