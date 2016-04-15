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

* win-unicode-console

Dev-dependencies
----------------

* bumpr
* wheel
* docutils
* twine
* setuptools

Changelog
---------

* 0.1.0 (Apr 15, 2016)

	- Initial release.
	