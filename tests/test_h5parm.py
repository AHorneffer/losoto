from __future__ import print_function
import sys
import unittest
import traceback
import tempfile
import os
import numpy as np
# import numpy.testing as nptest

# Append the path of the module to the syspath
# TODO: Refactor later

sys.path.append('../losoto')
from losoto.h5parm import h5parm, solFetcher, solWriter


class TestH5parm(unittest.TestCase):
    """
    Test the creation, reading and writing of h5parm files and the creation of solutions
    """

    def test_create_h5(self):
        """
        Test the creation of a h5parm file
        """
        try:
            H5 = h5parm('test.h5', readonly=False)
            del H5
            if os.path.isfile('test.h5'):
                os.remove('test.h5')
        except:
            self.fail(traceback.format_exc())

    def test_open_h5_readonly(self):
        """
        Test if the file can be opened in readonly mode
        """
        try:
            H5 = h5parm('test.h5', readonly=False)
            del H5
            H5 = h5parm('test.h5', readonly=True)
            del H5
            if os.path.isfile('test.h5'):
                os.remove('test.h5')
        except:
            self.fail(traceback.format_exc())

    def test_create_soltest(self):
        try:
            H5 = h5parm('test.h5', readonly=False)
            H5.makeSolset('ssTest')
            H5.makeSolset('ssTest')
            H5.makeSolset()
            del H5
            if os.path.isfile('test.h5'):
                os.remove('test.h5')
        except:
            self.fail(traceback.format_exc())

    def test_get_solset(self):
        try:
            H5 = h5parm('test.h5', readonly=False)
            H5.makeSolset('ssTest')
            H5.makeSolset('ssTest')
            H5.makeSolset()
            H5.getSolset('ssTest')
            del H5
            if os.path.isfile('test.h5'):
                os.remove('test.h5')
        except:
            self.fail(traceback.format_exc())


class TestH5parmSolutions(unittest.TestCase):
    """
    Based on a h5parm file with a solset named ssTest.
    Test of getAnt, getSou, getSolsets, and the creation of soltabs
    """

    def setUp(self):
        self.name = tempfile.mktemp(suffix=".h5")
        self.H5 = h5parm(self.name, readonly=False)
        self.ss = self.H5.makeSolset('ssTest')

    # def test_get_solset(self):
    #     try:
    #         self.H5.getSolset('ssTest')
    #     except:
    #         self.fail(traceback.format_exc())

    def test_get_ant(self):
        try:
            self.H5.getAnt(self.ss)
        except:
            self.fail(traceback.format_exc())

    def test_get_sources(self):
        try:
            self.H5.getSou(self.ss)
        except:
            self.fail(traceback.format_exc())

    def test_get_all_solsets(self):
        try:
            self.H5.getSolsets()
        except:
            self.fail(traceback.format_exc())

    def test_create_soltabs(self):
        """
        Create soltabs (using same names)
        """
        try:
            axesVals = [['a','b','c','d'], np.arange(100), np.arange(1000)]
            vals = np.arange(4*100*1000).reshape(4,100,1000)
            self.H5.makeSoltab(self.ss, 'amplitude', 'stTest', axesNames=['axis1','axis2','axis3'],
                               axesVals=axesVals, vals=vals, weights=vals)
            self.H5.makeSoltab(self.ss, 'amplitude', 'stTest', axesNames=['axis1','axis2','axis3'],
                               axesVals=axesVals, vals=vals, weights=vals)
            self.H5.makeSoltab(self.ss, 'amplitude', axesNames=['axis1','axis2','axis3'],
                               axesVals=axesVals, vals=vals, weights=vals)
        except:
            self.fail(traceback.format_exc())

    def TearDown(self):
        del self.H5
        if os.path.isfile(self.name):
            os.remove(self.name)


class TestH5parmSoltabs(unittest.TestCase):
    """
    Test the functionality of the soltabs
    """

    def setUp(self):
        self.name = tempfile.mktemp(suffix=".h5")
        self.H5 = h5parm(self.name, readonly=False)
        self.ss = self.H5.makeSolset('ssTest')
        axesVals = [['a','b','c','d'], np.arange(100), np.arange(1000)]
        vals = np.arange(4*100*1000).reshape(4,100,1000)
        self.H5.makeSoltab(self.ss, 'amplitude', 'stTest', axesNames=['axis1','axis2','axis3'],
                            axesVals=axesVals, vals=vals, weights=vals)
        self.H5.makeSoltab(self.ss, 'amplitude', 'stTest', axesNames=['axis1','axis2','axis3'],
                            axesVals=axesVals, vals=vals, weights=vals)
        self.H5.makeSoltab(self.ss, 'amplitude', axesNames=['axis1','axis2','axis3'],
                            axesVals=axesVals, vals=vals, weights=vals)

    def test_get_soltabs(self):
        """
        Get a soltab object
        """
        try:
            self.H5.getSoltab(self.ss, 'stTest')
        except:
            self.fail(traceback.format_exc())

    def test_get_all_soltabs(self):
        """
        Get all soltabs
        """
        try:
            self.H5.getSoltabs(self.ss)
        except:
            self.fail(traceback.format_exc())

    def test_print_info(self):
        try:
            self.H5.printInfo()
        except:
            self.fail(traceback.format_exc())

    def TearDown(self):
        del self.H5
        if os.path.isfile(self.name):
            os.remove(self.name)


class TestH5parmFetcherWriterCreation(unittest.TestCase):
    """
    Test the call to the solFetcher and solWriter
    """

    def setUp(self):
        self.name = tempfile.mktemp(suffix=".h5")
        self.H5 = h5parm(self.name, readonly=False)
        self.ss = self.H5.makeSolset('ssTest')
        axesVals = [['a','b','c','d'], np.arange(100), np.arange(1000)]
        vals = np.arange(4*100*1000).reshape(4,100,1000)
        self.H5.makeSoltab(self.ss, 'amplitude', 'stTest', axesNames=['axis1','axis2','axis3'],
                            axesVals=axesVals, vals=vals, weights=vals)
        self.H5.makeSoltab(self.ss, 'amplitude', axesNames=['axis1','axis2','axis3'],
                            axesVals=axesVals, vals=vals, weights=vals)
        self.st = self.H5.getSoltab(self.ss, 'stTest')

    def test_sol_fetcher(self):
        try:
            self.Hsf = solFetcher(self.st)
        except:
            self.fail(traceback.format_exc())

    def test_sol_writer(self):
        try:
            self.Hsw = solWriter(self.st)
        except:
            self.fail(traceback.format_exc())

    def TearDown(self):
        del self.H5
        if os.path.isfile(self.name):
            os.remove(self.name)


class TestH5parmFetcher(unittest.TestCase):
    """
    Test Hsf (solFetcher)
    """

    def setUp(self):
        self.name = tempfile.mktemp(suffix=".h5")
        self.H5 = h5parm(self.name, readonly=False)
        self.ss = self.H5.makeSolset('ssTest')
        axesVals = [['a','b','c','d'], np.arange(100), np.arange(1000)]
        vals = np.arange(4*100*1000).reshape(4,100,1000)
        self.H5.makeSoltab(self.ss, 'amplitude', 'stTest', axesNames=['axis1','axis2','axis3'],
                            axesVals=axesVals, vals=vals, weights=vals)
        self.H5.makeSoltab(self.ss, 'amplitude', axesNames=['axis1','axis2','axis3'],
                            axesVals=axesVals, vals=vals, weights=vals)
        self.st = self.H5.getSoltab(self.ss, 'stTest')
        self.Hsf = solFetcher(self.st)

    def test_get_axes_names(self):
        """
        Get Axes Names
        """
        try:
            self.Hsf.getAxesNames()
        except:
            self.fail(traceback.format_exc())

    def test_get_axes_len(self):
        """
        Get Axes1 Len (exp 4)
        """
        # TODO: Write assertion
        try:
            self.Hsf.getAxisLen('axis1')
        except:
            self.fail(traceback.format_exc())

    def test_get_type(self):
        """
        Get solution Type (exp: amplitude)
        """
        # TODO: Write assertion
        try:
            self.Hsf.getType()
        except:
            self.fail(traceback.format_exc())

    def test_get_axis_values(self):
        """
        Get axisValues (exp: a,b,c,d)
        """
        # TODO: Write assertion
        try:
            self.Hsf.getAxisValues('axis1')
        except:
            self.fail(traceback.format_exc())

    def test_set_selection(self):
        """
        Set a selection using single/multiple vals and append (exp: 1x1x2)
        """
        # TODO: Write assertion
        try:
            self.Hsf.setSelection(axis1='a', axis2=1, axis3=[1,10])
            v, a = self.Hsf.getValues()
        except:
            self.fail(traceback.format_exc())

    def test_set_selection2(self):
        """
        Set a selection using min max (exp: 4x10x10)
        """
        # TODO: Write assertion
        try:
            self.Hsf.setSelection(axis2={'min':10,'max':19}, axis3={'min':990, 'max':1e6})
            v, a = self.Hsf.getValues()
        except:
            self.fail(traceback.format_exc())

    def def_get_values_iter(self):
        """
        Get Vaues Iter (exp: 40 and 10)
        """
        # TODO: Write assertions
        try:
            i = 0
            for matrix, coord in self.Hsf.getValuesIter(returnAxes=['axis3']):
                i += 1
            i = 0
            for matrix, coord in self.Hsf.getValuesIter(returnAxes=['axis2','axis3']):
                i += 1
        except:
            self.fail(traceback.format_exc())

    def TearDown(self):
        del self.H5
        if os.path.isfile(self.name):
            os.remove(self.name)


class TestH5parmWriter(unittest.TestCase):
    """
    Test Hsw (solWriter)
    """

    def setUp(self):
        self.name = tempfile.mktemp(suffix=".h5")
        self.H5 = h5parm(self.name, readonly=False)
        self.ss = self.H5.makeSolset('ssTest')
        axesVals = [['a','b','c','d'], np.arange(100), np.arange(1000)]
        vals = np.arange(4*100*1000).reshape(4,100,1000)
        self.H5.makeSoltab(self.ss, 'amplitude', 'stTest', axesNames=['axis1','axis2','axis3'],
                            axesVals=axesVals, vals=vals, weights=vals)
        self.H5.makeSoltab(self.ss, 'amplitude', axesNames=['axis1','axis2','axis3'],
                            axesVals=axesVals, vals=vals, weights=vals)
        self.st = self.H5.getSoltab(self.ss, 'stTest')
        self.Hsf = solFetcher(self.st)
        self.Hsw = solWriter(self.st)

    def test_set_axis_values(self):
        """
        Get axisValues (exp: e,f,g,h)
        """
        # TODO: Write assertion
        try:
            self.Hsw.setAxisValues('axis1',['e','f','g','h'])
            self.Hsf.getAxisValues('axis1')
        except:
            self.fail(traceback.format_exc())


    def test_write_selection(self):
        """
        Writing back with selection
        """
        try:
            self.Hsw.setAxisValues('axis1',['e','f','g','h'])
            self.Hsf.setSelection(axis2={'min':10,'max':19}, axis3={'min':990, 'max':1e6})
            v, a = self.Hsf.getValues()
            self.Hsw.setSelection(axis1='e', axis2={'min':10,'max':19}, axis3={'min':990, 'max':1e6})
            self.Hsw.setValues(v[0])
        except:
            self.fail(traceback.format_exc())

    def test_history(self):
        """
        Set/Get history
        """
        try:
            self.Hsw.addHistory('history is working.')
            self.Hsw.getHistory()
        except:
            self.fail(traceback.format_exc())

    def TearDown(self):
        del self.H5
        if os.path.isfile(self.name):
            os.remove(self.name)


if __name__ == '__main__':
  unittest.main()