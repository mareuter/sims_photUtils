import unittest
import lsst.utils.tests as utilsTests
import numpy

from lsst.sims.photUtils import CosmologyWrapper

class CosmologyUnitTest(unittest.TestCase):

    def testFlatLCDM(self):
        w0=-1.0
        wa=0.0

        matter = numpy.arange(start=0.1, stop=0.5, step=0.1)
        hubble = numpy.arange(start=50.0, stop=90.0, step=5.0)

        for Om0 in matter:
            for H0 in hubble:
                Ode0 = 1.0 - Om0

                universe = CosmologyWrapper()
                universe.Initialize(H0=H0, Om0=Om0, Ode0=Ode0, w0=w0, wa=wa)

                Og0 = universe.OmegaPhotons(redshift=0.0)
                Onu0 = universe.OmegaNeutrinos(redshift=0.0)

                self.assertTrue(Og0 < 1.0e-4)
                self.assertTrue(Onu0 < 1.0e-4)
                self.assertAlmostEqual(universe.OmegaMatter(redshift=0.0), Om0, 10)
                self.assertAlmostEqual(Ode0 - universe.OmegaDarkEnergy(redshift=0.0), Og0+Onu0, 6)
                self.assertAlmostEqual(universe.H(redshift=0.0),H0,10)
                self.assertEqual(universe.OmegaCurvature(),0.0)

                Om0 = universe.OmegaMatter(redshift=0.0)
                Ode0 = universe.OmegaDarkEnergy(redshift=0.0)

                ztest = numpy.arange(start=0.0, stop=4.0, step=0.1)
                for zz in ztest:
                   aa = (1.0+zz)
                   Ototal = Om0*numpy.power(aa,3) + (Og0 +Onu0)*numpy.power(aa,4) + Ode0
                   OmControl = Om0*numpy.power(aa,3)/Ototal
                   self.assertAlmostEqual(OmControl, universe.OmegaMatter(redshift=zz), 6)

                   OdeControl = Ode0/Ototal
                   self.assertAlmostEqual(OdeControl, universe.OmegaDarkEnergy(redshift=zz), 6)

                   OgControl = Og0*numpy.power(aa,4)/Ototal
                   self.assertAlmostEqual(OgControl, universe.OmegaPhotons(redshift=zz), 6)

                   OnuControl = Onu0*numpy.power(aa,4)/Ototal
                   self.assertAlmostEqual(OnuControl, universe.OmegaNeutrinos(redshift=zz), 6)

                   Hcontrol = H0*numpy.sqrt(Ototal)
                   self.assertAlmostEqual(Hcontrol, universe.H(redshift=zz), 6)

                del universe

def suite():
    utilsTests.init()
    suites = []
    suites += unittest.makeSuite(CosmologyUnitTest)
    return unittest.TestSuite(suites)

def run(shouldExit = False):
    utilsTests.run(suite(),shouldExit)

if __name__ == "__main__":
    run(True)
