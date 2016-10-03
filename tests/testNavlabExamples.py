
# -*- coding: utf-8 -*-

'''NavLab examples

This page illustrates implementations of the examples from
<http://www.navlab.net/nvector>.  Values are chosen to match
those used in nvector.readthedocs.org.  Tests marked with
# +++ are additional, not present in the original examples.
'''
__version__ = '16.10.03'

if __name__ == '__main__':

    from tests import Tests

    from geodesy import Datums, F_D, \
                        ellipsoidalNvector, ellipsoidalVincenty, \
                        sphericalNvector, sphericalTrigonometry

    class Examples(Tests):  # overload test()
        def test(self, ex, name, *args, **kwds):
            name = 'Example %s %s' % (ex, name)
            Tests.test(self, name, *args, **kwds)

    t = Examples(__file__, __version__)

# Example 1: A and B to delta
    a = ellipsoidalNvector.LatLon(1, 2, 3)  # defaults to WGS-84
    b = ellipsoidalNvector.LatLon(4, 5, 6)
    delta = a.deltaTo(b)
    t.test(1, 'delta', delta, '[N:331730.863, E:332998.501, D:17398.304]')
    t.test(1, 'delta', delta.toStr2(prec=3), '[L:470357.384, B:45.109°, E:-2.12°]')  # +++
    t.test(1, 'elevation', delta.elevation, '-2.1198', fmt='%.4f')
    t.test(1, 'bearing', delta.bearing, '45.109', fmt='%.3f')  # 45.109°
    t.test(1, 'length', delta.length, '470357.384', fmt='%.3f')  # 470357.384 m

# Example 2: B and delta to C*
    n = ellipsoidalNvector.Nvector(1, 2, 3, 400, Datums.WGS72)
#   t.test(2, 'Nvector', n.toStr(prec=3), '[1.0, 2.0, 3.0, +400.00]')
    b = n.toLatLon()
    t.test(2, 'LatLon', b.toStr(F_D, prec=3), '53.301°N, 063.435°E, +400.00m')
    t.test(2, 'toNvector', b.toNvector().toStr(prec=3), '(0.267, 0.535, 0.802, +400.00)')
    delta = ellipsoidalNvector.Ned(3000, 2000, 100)
    t.test(2, 'delta', delta, '[N:3000.0, E:2000.0, D:100.0]')  # ++
    t.test(2, 'delta', delta.toStr2(prec=3), '[L:3606.938, B:33.69°, E:-1.589°]')  # +++
    c = b.destinationPoint(delta)
    t.test(2, 'destinationPoint', c.toStr(F_D), '53.327726°N, 063.464965°E, +299.138m')

    a = ellipsoidalNvector.LatLon(49.66618, 3.45063)  # ++
    b = ellipsoidalNvector.LatLon(48.88667, 2.37472)  # ++
    delta = a.deltaTo(b)  # ++
    t.test(2, 'delta', delta.toStr(prec=0), '[N:-86126, E:-78900, D:1069]')  # ++
    t.test(2, 'delta', delta.toStr2(prec=3), '[L:116807.681, B:222.493°, E:-0.524°]')  # +++
    c = a.destinationNed(delta)
    t.test(2, 'destinationPoint', c.toStr(F_D), '48.88667°N, 002.37472°E')

# Example 3: ECEF-vector to geodetic latitude
    c = ellipsoidalNvector.Cartesian(0.9*6371e3, -1.0*6371e3, 1.1*6371e3)
#   t.test(3, 'Cartesian', c, '[5733900.0, -6371000.0, 7008100.0]')
    p = c.toLatLon()
    t.test(3, 'toLatLon', p.toStr(F_D, prec=3), '39.379°N, 048.013°W, +4702059.83m')

# Example 4: Geodetic latitude to ECEF-vector
    p = ellipsoidalNvector.LatLon(1, 2, 3)
    c = p.toCartesian()
    t.test(4, 'toCartesian', c.toStr(prec=3), '[6373290.277, 222560.201, 110568.827]')

# Example 5: Surface distance
    a = sphericalNvector.LatLon(88, 0)
    b = sphericalNvector.LatLon(89, -170)
    dist = a.distanceTo(b)
    t.test(5, 'distanceTo', dist, '332457', fmt='%.0f')  # 332,457 m == 332.5 km

# Example 6: Interpolated position
    a = sphericalNvector.LatLon(89, 0)
    b = sphericalNvector.LatLon(89, 180)
    p = a.intermediateTo(b, 0.6)
    t.test(6, 'intermediateTo', p.toStr(F_D), '89.799981°N, 180.0°E')

    a = sphericalNvector.LatLon(52.205, 0.119)  # +++
    b = sphericalNvector.LatLon(48.857, 2.351)
    p = a.intermediateTo(b, 0.25)
    t.test(6, 'intermediateTo', p.toStr(F_D), '51.372294°N, 000.707192°E')  # 51.3723°N, 000.7072°E

# Example 7: Mean position
    points = [sphericalNvector.LatLon(90,   0),
              sphericalNvector.LatLon(60,  10),
              sphericalNvector.LatLon(50, -20)]
    mean = sphericalNvector.meanOf(points)  # XXX meanOf
    t.test(7, 'meanOf', mean.toStr(F_D, prec=4), '67.2362°N, 006.9175°W')
#   t.test(7, 'meanOfLatLon', mean.__class__, "<class 'sphericalNvector.LatLon'>")  # ++

# Example 8: A and azimuth/distance to B
    a = sphericalNvector.LatLon(80, -90)
    b = a.destinationPoint(1000, 200)
    t.test(8, 'destinationPoint(sphNv)', b.toStr(F_D), '79.991549°N, 090.017698°W')

    a = sphericalTrigonometry.LatLon(80, -90)  # +++
    b = a.destinationPoint(1000, 200)
    t.test(8, 'destinationPoint(sphTy)', b.toStr(F_D), '79.991549°N, 090.017698°W')

    a = ellipsoidalVincenty.LatLon(80, -90)  # +++
    b = a.destination(1000, 200)
    t.test(8, 'destination(elVincenty)', b.toStr(F_D), '79.991584°N, 090.017621°W')

# Example 9: Intersection of two paths
    a1 = sphericalNvector.LatLon(10, 20)
    a2 = sphericalNvector.LatLon(30, 40)
    b1 = sphericalNvector.LatLon(50, 60)
    b2 = sphericalNvector.LatLon(70, 80)
    c = sphericalNvector.intersection(a1, a2, b1, b2)
    t.test(9, 'intersection', c, '40.318643°N, 055.901868°E')

# Example 10: Cross track distance
    a1 = sphericalNvector.LatLon( 0, 0)
    a2 = sphericalNvector.LatLon(10, 0)
    b = sphericalNvector.LatLon(1, 0.1)
    c = b.crossTrackDistanceTo(a1, a2)
    t.test(10, 'crossTrackDistance', c, '11118', fmt='%.0f')  # 11,118 m == 11.12 km

    t.results()

    # Typical test results (on MacOS X):

    # testing testNavlabExamples.py version 16.10.03
    # test 1 Example 1 delta: [N:331730.863, E:332998.501, D:17398.304]
    # test 2 Example 1 delta: [L:470357.384, B:45.109°, E:-2.12°]
    # test 3 Example 1 elevation: -2.1198
    # test 4 Example 1 bearing: 45.109
    # test 5 Example 1 length: 470357.384
    # test 6 Example 2 LatLon: 53.301°N, 063.435°E, +400.00m
    # test 7 Example 2 toNvector: (0.267, 0.535, 0.802, +400.00)
    # test 8 Example 2 delta: [N:3000.0, E:2000.0, D:100.0]
    # test 9 Example 2 delta: [L:3606.938, B:33.69°, E:-1.589°]
    # test 10 Example 2 destinationPoint: 53.327726°N, 063.464965°E, +301.02m  FAILED, expected 53.327726°N, 063.464965°E, +299.138m
    # test 11 Example 2 delta: [N:-86126, E:-78900, D:1069]
    # test 12 Example 2 delta: [L:116807.681, B:222.493°, E:-0.524°]
    # test 13 Example 2 destinationPoint: 48.88667°N, 002.37472°E
    # test 14 Example 3 toLatLon: 39.379°N, 048.013°W, +4702059.83m
    # test 15 Example 4 toCartesian: [6373290.277, 222560.201, 110568.827]
    # test 16 Example 5 distanceTo: 332457
    # test 17 Example 6 intermediateTo: 89.799981°N, 180.0°E
    # test 18 Example 6 intermediateTo: 51.372294°N, 000.707192°E
    # test 19 Example 7 meanOf: 67.2362°N, 006.9175°W
    # test 20 Example 8 destinationPoint(sphNv): 79.991549°N, 090.017698°W
    # test 21 Example 8 destinationPoint(sphTy): 79.991549°N, 090.017698°W
    # test 22 Example 8 destination(elVincenty): 79.991584°N, 090.017621°W
    # test 23 Example 9 intersection: 40.318643°N, 055.901868°E
    # test 24 Example 10 crossTrackDistance: 11118
    # 1 testNavlabExamples.py test (4.2%) FAILED (Python 2.7.10)

    # testing testNavlabExamples.py version 16.10.03
    # test 1 Example 1 delta: [N:331730.863, E:332998.501, D:17398.304]
    # test 2 Example 1 delta: [L:470357.384, B:45.109°, E:-2.12°]
    # test 3 Example 1 elevation: -2.1198
    # test 4 Example 1 bearing: 45.109
    # test 5 Example 1 length: 470357.384
    # test 6 Example 2 LatLon: 53.301°N, 063.435°E, +400.00m
    # test 7 Example 2 toNvector: (0.267, 0.535, 0.802, +400.00)
    # test 8 Example 2 delta: [N:3000.0, E:2000.0, D:100.0]
    # test 9 Example 2 delta: [L:3606.938, B:33.69°, E:-1.589°]
    # test 10 Example 2 destinationPoint: 53.327726°N, 063.464965°E, +301.02m  FAILED, expected 53.327726°N, 063.464965°E, +299.138m
    # test 11 Example 2 delta: [N:-86126, E:-78900, D:1069]
    # test 12 Example 2 delta: [L:116807.681, B:222.493°, E:-0.524°]
    # test 13 Example 2 destinationPoint: 48.88667°N, 002.37472°E
    # test 14 Example 3 toLatLon: 39.379°N, 048.013°W, +4702059.83m
    # test 15 Example 4 toCartesian: [6373290.277, 222560.201, 110568.827]
    # test 16 Example 5 distanceTo: 332457
    # test 17 Example 6 intermediateTo: 89.799981°N, 180.0°E
    # test 18 Example 6 intermediateTo: 51.372294°N, 000.707192°E
    # test 19 Example 7 meanOf: 67.2362°N, 006.9175°W
    # test 20 Example 8 destinationPoint(sphNv): 79.991549°N, 090.017698°W
    # test 21 Example 8 destinationPoint(sphTy): 79.991549°N, 090.017698°W
    # test 22 Example 8 destination(elVincenty): 79.991584°N, 090.017621°W
    # test 23 Example 9 intersection: 40.318643°N, 055.901868°E
    # test 24 Example 10 crossTrackDistance: 11118
    # 1 testNavlabExamples.py test (4.2%) FAILED (Python 3.5.1)
