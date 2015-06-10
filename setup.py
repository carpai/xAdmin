import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'pyramid_debugtoolbar_ajax',
    'pyramid_debugtoolbar_mongo',
    'waitress',
    'pymongo==2.8.1',
    'mongokit',
    'mongokit-py3',
    'pycrypto',
    'pyramid_rpc'
    ]

setup(name='xAdmin',
      version='0.0',
      description='xAdmin',
      long_description=README.md + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="xadmin",
      entry_points="""\
      [paste.app_factory]
      main = xadmin:main
      """,
      )
