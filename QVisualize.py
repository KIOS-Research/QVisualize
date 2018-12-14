# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QVisualize
                                 A QGIS plugin
 Visualize a layer on canvas map
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-12-06
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Marios S. Kyriakou, KIOS Research and Innovation Center of Excellence (KIOS CoE)
        email                : mariosmsk@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import (QSettings, QTranslator, qVersion, QCoreApplication, QVariant, Qt)
from PyQt5.QtGui import (QIcon)
from PyQt5.QtWidgets import (QAction, QTableWidgetItem, QDockWidget, QProgressBar, QMessageBox, QWidget, QFileDialog)
from qgis.core import (QgsVectorLayer, QgsCoordinateReferenceSystem, QgsTask, QgsProject, QgsMessageLog, QgsApplication, QgsField,
                       QgsWkbTypes, QgsFeature)
from qgis.utils import Qgis

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .QVisualize_dialog import QVisualizeDialog
import os.path

# QVisualize
from time import sleep
MESSAGE_CATEGORY = 'QVisualize'

class QVisualize:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'QVisualize_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = QVisualizeDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&QVisualize')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'QVisualize')
        self.toolbar.setObjectName(u'QVisualize')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('QVisualize', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/qvisualize/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'QVisualize'),
            callback=self.run,
            parent=self.iface.mainWindow())

        self.dlg.start.clicked.connect(self.start)
        self.dlg.close_btn.clicked.connect(self.close)
        self.dlg.allfeature.clicked.connect(self.allfeature)
        self.dlg.finalfeature.clicked.connect(self.finalfeature)

        self.canvas = self.iface.mapCanvas()

    def finalfeature(self):
        pass

    def allfeature(self):
        pass

    def close(self):
        self.dlg.close()

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&QVisualize'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def run_task(self, task, wait_time):
        attr = [QgsField('fid', QVariant.String)]
        self.temp_data.addAttributes(attr)
        self.temp.updateFields()

        FEATURES = self.selected_layer.getFeatures()
        if not self.show__all_data:
            for i, elem in enumerate(FEATURES):
                feat = QgsFeature()
                self.temp.startEditing()
                feat.setGeometry(elem.geometry())
                feat.setAttributes([str(i)])
                self.temp.addFeatures([feat])
                self.temp.commitChanges()

                for feat_tmp in self.temp.getFeatures():
                    break
                break
        else:
            feat_tmp = QgsFeature()

        if self.show__all_data:
            self.temp.startEditing()
        for i, elem in enumerate(FEATURES):
            task.setProgress((i/self.total)*100)
            if not self.show__all_data:
                self.temp.startEditing()
                self.temp.changeGeometry(feat_tmp.id(), elem.geometry())
                self.temp.commitChanges()
            else:
                feat_tmp.setGeometry(elem.geometry())
                feat_tmp.setAttributes([str(i)])
                self.temp.addFeatures([feat_tmp])

            sleep(wait_time)
            self.temp.triggerRepaint()

            if task.isCanceled():
                self.stopped(task)
                return None
        self.temp.commitChanges()

    def stopped(self, task):
        try:
            self.temp.commitChanges()
        except:
            pass
        QgsMessageLog.logMessage(
            'Task "{name}" was canceled'.format(
                name=task.description()),
            MESSAGE_CATEGORY, Qgis.Info)

    def completed(self, exception, result=None):
        """This is called when doSomething is finished.
        Exception is not None if doSomething raises an exception.
        Result is the return value of doSomething."""
        if exception is None:
            if result is None:
                QgsMessageLog.logMessage(
                    'Completed with no exception and no result ' \
                    '(probably manually canceled by the user)',
                    MESSAGE_CATEGORY, Qgis.Warning)
            else:
                QgsMessageLog.logMessage(
                    'Task {name} completed\n'
                    'Total: {total} ( with {iterations} '
                    'iterations)'.format(
                        name=result['task'],
                        total=result['total'],
                        iterations=result['iterations']),
                    MESSAGE_CATEGORY, Qgis.Info)
        else:
            QgsMessageLog.logMessage("Exception: {}".format(exception),
                                     MESSAGE_CATEGORY, Qgis.Critical)
            raise exception

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.comboBox.clear()
        self.project = QgsProject.instance()

        # Initial layer list
        self.layer_list_name = []
        self.layer_list = []
        self.shp_type = 'Point'
        for layer in self.canvas.layers():
            if layer.type() == 0: #vectorlayer
                if layer.wkbType() == 1 or layer.wkbType() == 3 or layer.wkbType() == 6 or layer.wkbType() == 3001:
                    self.layer_list_name.append(layer.name())
                    self.layer_list.append(layer)

        self.dlg.comboBox.addItems(self.layer_list_name)
        self.dlg.show()

    def start(self):
        # Layer selection
        self.currentLayer = self.dlg.comboBox.currentText()
        if self.currentLayer == '':
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('QVisualize')
            msgBox.setText('Select a point/polygon layer.')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
            msgBox.exec_()
            return

        self.selected_layer_index = self.layer_list_name.index(self.currentLayer)
        self.selected_layer = self.layer_list[self.selected_layer_index]
        self.iface.setActiveLayer(self.selected_layer)

        if self.selected_layer.wkbType() == 3:
            self.shp_type = 'Polygon'
        if self.selected_layer.wkbType() == 6:
            self.shp_type = 'MultiPolygon'
        if self.selected_layer.wkbType() == 3001:
            self.shp_type = 'PointZM'

        self.total = self.selected_layer.featureCount()
        # Time delay
        time_delay = self.dlg.time_delay.value()

        # All features or final show
        if self.dlg.allfeature.isChecked():
            self.show__all_data = True
        if self.dlg.finalfeature.isChecked():
            self.show__all_data = False

        self.selected_layer.saveNamedStyle(self.plugin_dir + "\\tmp.qml")
        self.project.layerTreeRoot().findLayer(self.selected_layer.id()).setItemVisibilityChecked(False)

        self.temp = QgsVectorLayer(self.shp_type+"?crs=" + self.selected_layer.crs().authid(), self.currentLayer+"_qvisualize", "memory")
        self.temp.loadNamedStyle(self.plugin_dir + "\\tmp.qml")

        self.temp_data = self.temp.dataProvider()
        self.project.addMapLayer(self.temp)
        task = QgsTask.fromFunction(u'QVisualize', self.run_task,
                                    on_finished=self.completed, wait_time=time_delay)
        QgsApplication.taskManager().addTask(task)
        self.dlg.close()
