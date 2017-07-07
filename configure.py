# The target Python installation.
py_platform = linux
py_inc_dir = %(sysroot)/usr/include/python%(py_major).%(py_minor)
py_pylib_dir = %(sysroot)/usr/lib/python%(py_major).%(py_minor)/config
py_pylib_lib = python%(py_major).%(py_minor)mu

# The target PyQt installation.
pyqt_module_dir = %(sysroot)/usr/lib/python%(py_major)/dist-packages
pyqt_bin_dir = %(sysroot)/usr/bin
pyqt_sip_dir = %(sysroot)/usr/share/sip/PyQt5
pyuic_interpreter = /usr/bin/python%(py_major).%(py_minor)
pyqt_disabled_features = PyQt_Desktop_OpenGL PyQt_qreal_double

# Qt configuration common to all versions.
qt_shared = True

[Qt 5.1]
pyqt_modules = QtCore QtDBus QtDesigner QtGui QtHelp QtMultimedia
    QtMultimediaWidgets QtNetwork QtOpenGL QtPrintSupport QtQml QtQuick
    QtSensors QtSerialPort QtSql QtSvg QtTest QtWebKit QtWebKitWidgets
    QtWidgets QtXmlPatterns _QOpenGLFunctions_ES2