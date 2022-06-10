with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='py-tools',
    version='0.0.1',
    author='Raffael @ Nice Pink',
    author_email='r@nice.pink',
    description='Python tools',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/nice-pink/py-tools',
    project_urls = {
        "Bug Tracker": "https://github.com/nice-pink/py-tools/issues"
    },
    license='MIT',
    packages=['tools'],
    install_requires=[],
)