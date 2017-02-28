#! python3

from xcute import cute, Exc

cute(
	pkg_name = "safeprint",
	test = [
		'py -3.5 -m pylint {pkg_name} setup.py cute.py',
		['py -{v} test.py && py -{v} test.py > %temp%/safeprint-test-{v}.txt'
			.format(v=v) for v in (2, 3.5, 3.6)],
		'readme_build'
	],
	bump_pre = 'test',
	bump_post = ['dist', 'release', 'publish', 'install'],
	dist = 'python setup.py sdist bdist_wheel',
	release = [
		'git add .',
		'git commit -m "Release v{version}"',
		'git tag -a v{version} -m "Release v{version}"'
	],
	publish = [
		'twine upload dist/*{version}[.-]*',
		'git push --follow-tags'
	],
	publish_err = 'start https://pypi.python.org/pypi/{pkg_name}/',
	install = 'pip install -e .',
	install_err = 'elevate -c -w pip install -e .',
	readme_build = 'python setup.py --long-description > %temp%/ld && '
		'rst2html --no-raw --exit-status=1 --verbose %temp%/ld %temp%/ld.html',
	readme_build_err = ['readme_show', Exc()],
	readme_show = 'start %temp%/ld.html',
	readme = 'readme_build',
	readme_post = 'readme_show'
)
