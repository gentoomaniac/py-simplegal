from pysimplegal.tests import *

class TestImageController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='view', action='index'))
        # Test response...
