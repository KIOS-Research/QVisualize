# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QVisualize
                                 A QGIS plugin
 Visualize a layer on canvas map
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2018-12-06
        copyright            : (C) 2018 by Marios S. Kyriakou, KIOS Research and Innovation Center of Excellence (KIOS CoE)
        email                : mariosmsk@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load QVisualize class from file QVisualize.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .QVisualize import QVisualize
    return QVisualize(iface)