import unittest

from enhancer.ZeroPointUtils import ZeroPointScaler

clipsrc = (2635955.3, 1256666.5, 2635997.8, 1256709.9)


class ZeroPointScalerPointTestCase(unittest.TestCase):

    def setUp(self):
        self.dataset = {'lkobject_type': 'lkpunkt',
                        'a': {'object_type': 4, 'object_owner': 'Bob', 'geometry': (2635982.637, 1256670.796),
                              'characteristics': {'Funktion': 'Sammelkanal', 'Nutzungsart': 'Regenabwasser'}}}
        self.point_scaler = ZeroPointScaler(self.dataset, clipsrc)
        geom_tuple = self.dataset['a']['geometry']
        self.expected_result = (geom_tuple[0] - clipsrc[0], geom_tuple[1] - clipsrc[1])

    def test_scale_objects(self):
        result = self.point_scaler.scale_point_objects()
        self.assertEquals(result['a']['geometry'], self.expected_result)


class ZeroPointScalerAreaTestCase(unittest.TestCase):

    def setUp(self):
        self.dataset = {'lkobject_type': 'lkflaeche',
                        'd': {'object_type': 4, 'object_owner': 'Bob',
                              'geometry': (((2635982.943, 1256671.321), (2635982.905, 1256671.34),
                                            (2635982.866, 1256671.354), (2635982.827, 1256671.365)),),
                              'characteristics': {'Funktion': 'Sammelkanal', 'Nutzungsart': 'Regenabwasser'}}}
        self.area_scaler = ZeroPointScaler(self.dataset, clipsrc)
        self.geom_tuples_d = self.dataset['d']['geometry']
        self.geom_tuples_scaled = ((round(self.dataset['d']['geometry'][0][0][0] - clipsrc[0], 4),
                                    round(self.dataset['d']['geometry'][0][0][1] - clipsrc[1], 4)),
                                   (round(self.dataset['d']['geometry'][0][1][0] - clipsrc[0], 4),
                                    round(self.dataset['d']['geometry'][0][1][1] - clipsrc[1], 4)),
                                   (round(self.dataset['d']['geometry'][0][2][0] - clipsrc[0], 4),
                                    round(self.dataset['d']['geometry'][0][2][1] - clipsrc[1], 4)),
                                   (round(self.dataset['d']['geometry'][0][3][0] - clipsrc[0], 4),
                                    round(self.dataset['d']['geometry'][0][3][1] - clipsrc[1], 4)))

    def test_scale_objects(self):
        result = self.area_scaler.scale_area_objects()
        self.assertEquals(self.geom_tuples_scaled, result['d']['geometry'])


class ZeroPointScalerLineTestCase(unittest.TestCase):

    def setUp(self):
        self.dataset = {'lkobject_type': 'lklinie',
                        'b': {'object_type': 4, 'object_owner': 'Bob',
                              'geometry': ((2635985.45, 1256676.406), (2635985.287, 1256675.673)),
                              'characteristics': {'Funktion': 'Sammelkanal', 'Nutzungsart': 'Regenabwasser'}},
                        'c': {'object_type': 4, 'object_owner': 'Bob',
                              'geometry': ((2635983.45, 1256676.403), (2635985.187, 1256675.573)),
                              'characteristics': {'Funktion': 'Sammelkanal', 'Nutzungsart': 'Regenabwasser'}},
                        }
        self.line_scaler = ZeroPointScaler(self.dataset, clipsrc)
        self.geom_tuples = (self.dataset['b']['geometry'], self.dataset['c']['geometry'])
        self.geom_tuples_scaled = (
            ((round(self.dataset['b']['geometry'][0][0] - clipsrc[0], 4),
              round(self.dataset['b']['geometry'][0][1] - clipsrc[1], 4)),
             (round(self.dataset['b']['geometry'][1][0] - clipsrc[0], 4),
              round(self.dataset['b']['geometry'][1][1] - clipsrc[1], 4))),
            ((round(self.dataset['c']['geometry'][0][0] - clipsrc[0], 4),
              round(self.dataset['c']['geometry'][0][1] - clipsrc[1], 4)),
             (round(self.dataset['c']['geometry'][1][0] - clipsrc[0], 4),
              round(self.dataset['c']['geometry'][1][1] - clipsrc[1], 4))))

    def test_scale_objects(self):
        result = self.line_scaler.scale_line_objects()
        result_tuple = (result['b']['geometry'], result['c']['geometry'])
        print(result_tuple)
        print("\n")
        print(self.geom_tuples_scaled)
        self.assertEquals(self.geom_tuples_scaled, result_tuple)


if __name__ == '__main__':
    unittest.main()
