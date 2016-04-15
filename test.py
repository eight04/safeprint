import timeit, functools, safeprint

texts = ["Hello World!", "你好世界！", "ハローワールド", "हैलो वर्ल्ड"]

def do_print(printer):
	printer.print(*texts)
	
results = []
for printer in (safeprint.EchoPrinter(), safeprint.TryPrinter(), safeprint.WinUnicodePrinter()):
	test = functools.partial(do_print, printer)

	result = timeit.timeit("test()", number=100, setup="from __main__ import test")
	results.append(result)
	
print(results)
