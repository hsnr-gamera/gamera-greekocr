from pathlib import Path

from setuptools import setup

from gamera import gamera_setup

# This constant should be the name of the toolkit
TOOLKIT_NAME = "greekocr"
VERSION = "2.0.0"
AUTHOR = "Rene Baston and Christoph Dalitz and Andreas Miller"
HOMEPAGE = "http://gamera.sourceforge.net/"
DESCRIPTION = "An addon Greek OCR toolkit for the Gamera framework for document analysis and recognition."
LICENSE = "GNU GPL version 3"

# ----------------------------------------------------------------------------
# You should not usually have to edit anything below, but it is
# implemented here and not in the Gamera core so that you can edit it
# if you need to do something more complicated (for example, building
# and linking to a third- party library).
# ----------------------------------------------------------------------------

PLUGIN_PATH = 'gamera/toolkits/%s/plugins/' % TOOLKIT_NAME
PACKAGE = 'gamera.toolkits.%s' % TOOLKIT_NAME
PLUGIN_PACKAGE = PACKAGE + ".plugins"
plugins = gamera_setup.get_plugin_filenames(PLUGIN_PATH)
plugin_extensions = gamera_setup.generate_plugins(plugins, PLUGIN_PACKAGE)

# This is a standard setuptools setup initializer. If you need to do
# anything more complex here, refer to the Python setuptools documentation.
if __name__ == "__main__":
    setup(name="gamera-greekocr",
          version=VERSION,
          license=LICENSE,
          url=HOMEPAGE,
          author=AUTHOR,
          description=DESCRIPTION,
          ext_modules=plugin_extensions,
          packages=[PACKAGE, PLUGIN_PACKAGE],
          include_dirs=['include/plugins'],
          python_requires='>=3.5',
          scripts=['scripts/greekocr4gamera'],
          install_requires=['gamera>=4.1.0', 'gamera-ocr>=2.0.0']
          )
