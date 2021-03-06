# -*- coding: utf-8 -*-

"""
***************************************************************************
    fillnodata.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
from PyQt4 import QtGui, QtCore

from processing.core.GeoAlgorithm import GeoAlgorithm

from processing.parameters.ParameterRaster import ParameterRaster
from processing.parameters.ParameterNumber import ParameterNumber
from processing.parameters.ParameterBoolean import ParameterBoolean
from processing.outputs.OutputRaster import OutputRaster

from processing.tools.system import *

from processing.algs.gdal.GdalUtils import GdalUtils


class fillnodata(GeoAlgorithm):

    INPUT = 'INPUT'
    DISTANCE = 'DISTANCE'
    ITERATIONS = 'ITERATIONS'
    BAND = 'BAND'
    MASK = 'MASK'
    NO_DEFAULT_MASK = 'NO_DEFAULT_MASK'
    OUTPUT = 'OUTPUT'

    #def getIcon(self):
    #    filepath = os.path.dirname(__file__) + '/icons/fillnodata.png'
    #    return QtGui.QIcon(filepath)

    def defineCharacteristics(self):
        self.name = 'Fill nodata'
        self.group = '[GDAL] Analysis'
        self.addParameter(ParameterRaster(self.INPUT, 'Input layer', False))
        self.addParameter(ParameterNumber(self.DISTANCE, 'Search distance', 0,
                          9999, 100))
        self.addParameter(ParameterNumber(self.ITERATIONS, 'Smooth iterations'
                          , 0, 9999, 0))
        self.addParameter(ParameterNumber(self.BAND, 'Band to operate on', 1,
                          9999, 1))
        self.addParameter(ParameterRaster(self.MASK, 'Validity mask', True))
        self.addParameter(ParameterBoolean(self.NO_DEFAULT_MASK,
                          'Do not use default validity mask', False))

        self.addOutput(OutputRaster(self.OUTPUT, 'Output layer'))

    def processAlgorithm(self, progress):
        output = self.getOutputValue(self.OUTPUT)

        arguments = []
        arguments.append('-md')
        arguments.append(str(self.getParameterValue(self.DISTANCE)))

        if self.getParameterValue(self.ITERATIONS) != 0:
            arguments.append('-si')
            arguments.append(str(self.getParameterValue(self.ITERATIONS)))

        arguments.append('-b')
        arguments.append(str(self.getParameterValue(self.BAND)))

        mask = self.getParameterValue(self.MASK)
        if mask is not None:
            arguments.append('-mask')
            arguments.append(mask)

        if self.getParameterValue(self.NO_DEFAULT_MASK):
            arguments.append('-nomask')

        arguments.append('-of')
        arguments.append(GdalUtils.getFormatShortNameFromFilename(output))

        arguments.append(self.getParameterValue(self.INPUT))
        arguments.append(output)

        commands = []
        if isWindows():
            commands = ['cmd.exe', '/C ', 'gdal_fillnodata.bat',
                        GdalUtils.escapeAndJoin(arguments)]
        else:
            commands = ['gdal_fillnodata.py',
                        GdalUtils.escapeAndJoin(arguments)]

        GdalUtils.runGdal(commands, progress)
