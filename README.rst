safeprint
=========

A printer suppressing UnicodeEncodeError.

Installation
------------

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
	
	# create a printer
	printer = safeprint.Printer()
	
	def callback(text):
		# do something with the text
	
	printer.add_listener(callback)
	
	printer.print(1, 2, 3, sep=", ")
	
	printer.remove_listener(callback)

How it works
------------

Python 3
~~~~~~~~

* Printing to the console

  Before printing, python encodes your text based on the encoding of your console. It is usally "utf-8" in Linux. Under Windows, you can check your default code page by cmd command ``chcp``.
  
  As the result, if python can't encode your text with the encoding, "UnicodeEncodeError" is raised. You can solve this by switching console encoding - run command ``chcp 65001`` to switch to utf-8 before running python.
  
  What safeprint does, is to use `win-unicode-console <https://github.com/Drekin/win-unicode-console>`__. win-unicode-console uses WinAPI to write text to console.
  
  Also, after python 3.6, `python has builtin support for that <https://docs.python.org/3/whatsnew/3.6.html#pep-528-change-windows-console-encoding-to-utf-8>`__.
  
* Printing to a file (redirected output)

  This cause "UnicodeEncodeError" because, python use your system code page as default encoding for stdios. To solve this, you should set environment variable "PYTHONIOENCODING" to "utf-8", which makes python use utf-8 as the encoding. (https://docs.python.org/3/using/cmdline.html#envvar-PYTHONIOENCODING)
  
  What safeprint does, is just always encode your text in utf-8, and write the bytes to stdout directly.
  
Python 2
~~~~~~~~

In python 2, there is no difference between bytes and str. An str is just a series of bytes, which is what python actually read from your source code. If you write the same string but save in different source file with different encoding, python will get different series of bytes too.

* Printing to the console

  Since there is no difference between bytes and str, writing str to console is just writing bytes to console and will never raise an UnicodeEncodeError. However, you might get garbled if the encoding of the console doesn't match the encoding of the source code (and python 2 just doesn't work well with cp65001, switching code page might not work).
  
  When printing unicode text, python will try to convert unicode into bytes with the encoding of the console, just like python 3, which might result in UnicodeEncodeError.
  
  The solution is same as in python 3. safeprint use win-unicode-console to print unicode text.

* Printing to a file (redirected output)

  As we said, there is no difference between bytes and str. When printing a str to a file, is actually just writing a series of bytes to the file, which will never raise an UnicodeEncodeError.

  But, when printing an unicode object, python has to encode the unicode into bytes, based on the default encoding of python (you can check the default encoding by running this python script ``import sys; print(sys.getdefaultencoding())``, it defaults to "ascii" in python 2). As the result, the printing will fail with UnicodeEncodeError if python can't encode your unicode object.
  
  To solve this, you can set the environment variable "PYTHONIOENCODING" just like python 3, or encode your unicode object with utf-8 before sending to the print function, which is what safeprint does.

Changelog
---------

* 0.1.4 (Dec 31, 2016)

  - Make win-unicode-console optional with Python 3.6.

* 0.1.2 (Jul 21, 2016)

  - Compatible with win-unicode-console 0.5

* 0.1.1 (Apr 15, 2016)

  - Fix builtins bug.

* 0.1.0 (Apr 15, 2016)

  - Initial release.
	