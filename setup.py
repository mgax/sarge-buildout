import distutils.core


distutils.core.setup(
    name='sarge-buildout',
    version='0.1',
    install_requires=['Sarge'],
    py_modules=['sarge_buildout'],
    entry_points={'sarge_plugins': ['sarge_buildout=sarge_buildout:initialize']},
)
