# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QVisualize_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from qgis.PyQt import (QtGui, uic, QtCore)
from qgis.PyQt.QtWidgets import (QDialog)
import os

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui/QVisualize_dialog_base.ui'))


class QVisualizeDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        # """Constructor."""
        QDialog.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        super(QVisualizeDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect

        self.setupUi(self)