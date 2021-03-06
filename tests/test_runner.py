#
# Unittest code to run tests on single element models with DGD
#

import os
import shutil
import abaverify as av

# Helper for dealing with .props files
def copyMatProps():
    # If testOutput doesn't exist, create it
    testOutputPath = os.path.join(os.getcwd(), 'testOutput')
    if not os.path.isdir(testOutputPath):
        os.makedirs(testOutputPath)

    # Put a copy of the properties file in the testOutput directory
    propsFiles = [x for x in os.listdir(os.getcwd()) if x.endswith('.props')]
    for propsFile in propsFiles:
        shutil.copyfile(os.path.join(os.getcwd(), propsFile), os.path.join(os.getcwd(),'testOutput', propsFile))


def plotFailureEnvelope(baseName, abscissaIdentifier, ordinateIdentifier, abcissaStrengths, ordinateStrengths):
    """
    Create a plot of the failure envelope. Does noting if matplotlib import fails.
    """

    # Try to import matplotlib
    try:
        import matplotlib.pyplot as plt

        # Read the failure envelope data
        with open(os.path.join(os.getcwd(), 'testOutput', baseName + '_failure_envelope.txt'), 'r') as fe:
            data = dict()
            dataHeaders = list()
            for line in fe:
                lineSplit = line.split(', ')

                # Hanle the header row separately
                if len(data) == 0:
                    for i in range(0, len(lineSplit)):
                        data[lineSplit[i]] = list()
                        dataHeaders.append(lineSplit[i])
                else:
                    for i in range(0, len(lineSplit)):
                        data[dataHeaders[i]].append(lineSplit[i])

        # Plot the failure envelope
        fig = plt.figure()

        # Reference data
        dataRef = dict()
        dataRef[abscissaIdentifier] = abcissaStrengths + [0]*len(ordinateStrengths)
        dataRef[ordinateIdentifier] = [0]*len(abcissaStrengths) + ordinateStrengths
        plt.plot(dataRef[abscissaIdentifier], dataRef[ordinateIdentifier], 'x', markeredgecolor='black')

        # Data from CompDam
        plt.plot(data[abscissaIdentifier], data[ordinateIdentifier], 'o', markerfacecolor='none', markeredgecolor='#ED7D31')
        ax = plt.subplot(111)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        plt.xlabel(r'$\sigma_{' + abscissaIdentifier.split('S')[1] + '}$ [MPa]')
        plt.ylabel(r'$\sigma_{' + ordinateIdentifier.split('S')[1] + '}$ [MPa]')
        fig.savefig(os.path.join(os.getcwd(), 'testOutput', baseName + '.png'), dpi=300)

    # If import fails, the above code is skipped
    except ImportError:
        print "INFO: matplotlib package not found. Install matplotlib to generate plots of the failure envelope automatically."


class ParametricMixedModeMatrix(av.TestCase):
    """
    Parametric mixed mode tests.
    """

    # Specify meta class
    __metaclass__ = av.ParametricMetaClass

    # Refers to the template input file name
    baseName = "test_C3D8R_mixedModeMatrix"

    # Range of parameters to test; all combinations are tested
    # alpha is the angle of the crack normal
    # beta defines the direction of tensile loading in Step-1 and compressive loading in Step-2
    parameters = {'alpha': range(0,50,10), 'beta': range(0,210,30), 'friction': [0.00, 0.15, 0.30, 0.45, 0.60]}


class ParametricFailureEnvelope_sig12sig22(av.TestCase):
    """
    Generate failure envelope in the sigma12 - sigma22 space with a C3D8R element
    """

    # Specify meta class
    __metaclass__ = av.ParametricMetaClass

    # Refers to the template input file name
    baseName = "test_C3D8R_failureEnvelope_sig12sig22"

    # Range of parameters to test; all combinations are tested
    abcissaStrengths = [-199.8, 62.3]
    ordinateStrengths = [92.3]
    parameters = {'loadRatio':  [x/100. for x in range(0,101,5)], 'matrixStrength': abcissaStrengths}

    @classmethod
    def setUpClass(cls):
        copyMatProps()

    @classmethod
    def tearDownClass(cls):
        plotFailureEnvelope(baseName=cls.baseName, abscissaIdentifier='S22', ordinateIdentifier='S12', abcissaStrengths=cls.abcissaStrengths, ordinateStrengths=cls.ordinateStrengths)


class ParametricFailureEnvelope_sig12sig22_shell(av.TestCase):
    """
    Generate failure envelope in the sigma12 - sigma22 space with a S4R element
    """

    # Specify meta class
    __metaclass__ = av.ParametricMetaClass

    # Refers to the template input file name
    baseName = "test_S4R_failureEnvelope_sig12sig22"

    # Range of parameters to test; all combinations are tested
    abcissaStrengths = [-199.8, 62.3]
    ordinateStrengths = [92.3]
    parameters = {'loadRatio':  [x/100. for x in range(0,101,5)], 'matrixStrength': abcissaStrengths}

    @classmethod
    def setUpClass(cls):
        copyMatProps()

    @classmethod
    def tearDownClass(cls):
        plotFailureEnvelope(baseName=cls.baseName, abscissaIdentifier='S22', ordinateIdentifier='S12', abcissaStrengths=cls.abcissaStrengths, ordinateStrengths=cls.ordinateStrengths)


class ParametricFailureEnvelope_sig12sig23(av.TestCase):
    """
    Generate failure envelope in the sigma12 - sigma23 space
    """

    # Specify meta class
    __metaclass__ = av.ParametricMetaClass

    # Refers to the template input file name
    baseName = "test_C3D8R_failureEnvelope_sig12sig23"

    # Range of parameters to test; all combinations are tested
    abcissaStrengths = [92.3]
    ordinateStrengths = [75.3]
    parameters = {'loadRatio':  [x/100. for x in range(0,101,5)], 'matrixStrength': abcissaStrengths}


    @classmethod
    def setUpClass(cls):
        copyMatProps()

    @classmethod
    def tearDownClass(cls):
        plotFailureEnvelope(baseName=cls.baseName, abscissaIdentifier='S12', ordinateIdentifier='S23', abcissaStrengths=cls.abcissaStrengths, ordinateStrengths=cls.ordinateStrengths)


class ParametricFailureEnvelope_sig11sig22(av.TestCase):
    """
    Generate failure envelope in the sigma11 - sigma22 space with C3D8R element
    """

    # Specify meta class
    __metaclass__ = av.ParametricMetaClass

    # Refers to the template input file name
    baseName = "test_C3D8R_failureEnvelope_sig11sig22"

    # Range of parameters to test; all combinations are tested
    abcissaStrengths = [-1200.1, 2326.2]
    ordinateStrengths = [-199.8, 62.3]
    parameters = {'loadRatio':  [x/100. for x in range(0,101,10)], 'ordinateStrength': ordinateStrengths, 'abcissaStrength': abcissaStrengths}


    @classmethod
    def setUpClass(cls):
        copyMatProps()

    @classmethod
    def tearDownClass(cls):
        plotFailureEnvelope(baseName=cls.baseName, abscissaIdentifier='S11', ordinateIdentifier='S22', abcissaStrengths=cls.abcissaStrengths, ordinateStrengths=cls.ordinateStrengths)


class ParametricFailureEnvelope_sig11sig22_shell(av.TestCase):
    """
    Generate failure envelope in the sigma11 - sigma22 space with a S4R element
    """

    # Specify meta class
    __metaclass__ = av.ParametricMetaClass

    # Refers to the template input file name
    baseName = "test_S4R_failureEnvelope_sig11sig22"

    # Range of parameters to test; all combinations are tested
    abcissaStrengths = [-1200.1, 2326.2]
    ordinateStrengths = [-199.8, 62.3]
    parameters = {'loadRatio':  [x/100. for x in range(0,101,10)], 'ordinateStrength': ordinateStrengths, 'abcissaStrength': abcissaStrengths}


    @classmethod
    def setUpClass(cls):
        copyMatProps()

    @classmethod
    def tearDownClass(cls):
        plotFailureEnvelope(baseName=cls.baseName, abscissaIdentifier='S11', ordinateIdentifier='S22', abcissaStrengths=cls.abcissaStrengths, ordinateStrengths=cls.ordinateStrengths)


class ParametricKinkBandWidth_twoElement(av.TestCase):
    """
    Tests for fiber compression damage mode to ensure mesh objectivity
    Should yield the same response as ParametricKinkBandWidth_singleElement
    """

    # Class-wide methods
    @classmethod
    def setUpClass(cls):
        copyMatProps()

    # Specify meta class
    __metaclass__ = av.ParametricMetaClass

    # Refers to the template input file name
    baseName = "test_C3D8R_twoElement_fiberCompression_FKT"

    # Use python script instead of input file
    pythonScriptForModel = True

    # Range of parameters to test; all combinations are tested
    parameters = {'elasticElToTotal': [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]}

    # Crush stress is different for each kinkband size, so the expected values are specified here
    expectedpy_parameters = {'crushStress': [-7.9, -8.8, -9.6, -10.3, -11, -11.5]}


class ParametricKinkBandWidth_singleElement(av.TestCase):
    """
    Tests to show the effect of kinkband width relative to element size
    """

    # Class-wide methods
    @classmethod
    def setUpClass(cls):
        copyMatProps()

    # Specify meta class
    __metaclass__ = av.ParametricMetaClass

    # Refers to the template input file name
    baseName = "test_C3D8R_fiberCompression_FKT"

    # Range of parameters to test; all combinations are tested
    parameters = {'wkbToTotal': [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]}

    # Crush stress is different for each kinkband size, so the expected values are specified here
    expectedpy_parameters = {'crushStress': [-7.9, -8.8, -9.6, -10.3, -11, -11.5, -11.9]}

    # Ignore the displacement at peak load
    expectedpy_ignore = ('x_at_peak_in_xy')


class SingleElementTests(av.TestCase):
    """
    Single element models to tests the DGD code base
    """

    # Class-wide methods
    @classmethod
    def setUpClass(cls):
        copyMatProps()

    # -----------------------------------------------------------------------------------------
    # Test methods
    def test_C3D8R_matrixTension(self):
        """ Simple tension applied in the matrix direction, solid element """
        self.runTest("test_C3D8R_matrixTension")


    def test_C3D8R_simpleShear12(self):
        """ Simple shear in the 1-2 plane, solid element """
        self.runTest("test_C3D8R_simpleShear12")


    def test_C3D8R_simpleShear12friction(self):
        """ Compression followed by simple shear in the 1-2 plane, solid element """
        self.runTest("test_C3D8R_simpleShear12friction")


    def test_C3D8R_nonlinearShear12(self):
        """ Nonlinear shear model, loading and unloading, solid """
        self.runTest("test_C3D8R_nonlinearShear12")


    def test_C3D8R_fiberTension(self):
        """ Fiber tension, solid element """
        self.runTest("test_C3D8R_fiberTension")


    def test_C3D8R_fiberCompression_FKT(self):
        """ Fiber compression: Fiber kinking theory based model, solid element """
        self.runTest("test_C3D8R_fiberCompression_FKT")


    def test_C3D8R_fiberCompression_FKT_FN(self):
        """ Fiber compression: Fiber kinking theory based model, solid element, fiber nonlinearity """
        self.runTest("test_C3D8R_fiberCompression_FKT_FN")


    def test_C3D8R_fiberCompression_BL(self):
        """ Fiber compression: Bilinear softening based model, solid element """
        self.runTest("test_C3D8R_fiberCompression_BL")


    def test_C3D8R_fiberLoadReversal(self):
        """ Fiber damage model, Maimi: load reversal, solid element """
        self.runTest("test_C3D8R_fiberLoadReversal")


    def test_S4R_matrixTension(self):
        """ Simple tension applied in the matrix direction, shell element """
        self.runTest("test_S4R_matrixTension")


    def test_C3D8R_nonlinearShear12(self):
        """ Nonlinear shear model, loading and unloading """
        self.runTest("test_C3D8R_nonlinearShear12")


    def test_C3D8R_schapery12(self):
        """ Schapery micro-damage model, loading and unloading in 1--2 plane"""
        self.runTest("test_C3D8R_schapery12")


    def test_C3D8R_matrixCompression(self):
        """ Matrix compression """
        self.runTest("test_C3D8R_matrixCompression")


    def test_C3D8R_elastic_matrixTension(self):
        """ Elastic matrix tension """
        self.runTest("test_C3D8R_elastic_matrixTension")


    def test_C3D8R_elastic_fiberTension(self):
        """ Elastic fiber tension """
        self.runTest("test_C3D8R_elastic_fiberTension")


    def test_C3D8R_elementSize(self):
        """ User characteristic length """
        self.runTest("test_C3D8R_elementSize")


    def test_S4R_elementSize(self):
        """ User characteristic length, shell element """
        self.runTest("test_S4R_elementSize")


    def test_S4R_simpleShear12(self):
        """ Simple shear in the 1-2 plane, shell element"""
        self.runTest("test_S4R_simpleShear12")


    def test_S4R_simpleShear12friction(self):
        """ Compression followed by simple shear in the 1-2 plane, shell element """
        self.runTest("test_S4R_simpleShear12friction")


    def test_S4R_nonlinearShear12(self):
        """ Nonlinear shear model, loading and unloading, shell element """
        self.runTest("test_S4R_nonlinearShear12")


    def test_S4R_schapery12(self):
        """ Schapery micro-damage model, loading and unloading in 1--2 plane, shell element"""
        self.runTest("test_S4R_schapery12")


    def test_S4R_matrixCompression(self):
        """ Matrix compression """
        self.runTest("test_S4R_matrixCompression")


    def test_S4R_fiberTension(self):
        """ Fiber tension, shell element """
        self.runTest("test_S4R_fiberTension")


    def test_S4R_fiberCompression_BL(self):
        """ Fiber compression: Bilinear softening based model, shell element """
        self.runTest("test_S4R_fiberCompression_BL")


    def test_S4R_fiberLoadReversal(self):
        """ Fiber damage model, Maimi: load reversal, shell element """
        self.runTest("test_S4R_fiberLoadReversal")



if __name__ == "__main__":
    av.runTests(relPathToUserSub='../for/CompDam_DGD', double=True)
