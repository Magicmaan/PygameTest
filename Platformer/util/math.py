import math

from pygame import Vector2


def generate_curved_points(start, end, max_height, offset_x, num_points):
    # f = x * math.PI
    # x = sin( math.pow(f,offset_x+1) / math.pow(math.PI,offset_x))
    points: list[Vector2] = []

    is_negative = offset_x < 0

    distance = end.x - start.x
    offset_x = 1 + abs(offset_x)
    # y = math.pow(math.sin(math.pow(f, offset_x + 1) / math.pow(math.pi, offset_x)), 0.5)
    for i in range(num_points):
        x = i / num_points
        y = 0
        f = (x) * math.pi

        y = math.sin(f**offset_x / math.pow(math.pi, offset_x - 1))
        # y = math.sin(math.pow(f, offset_x + 1) / math.pow(math.pi, offset_x))
        y = math.pow(y, 0.25) * max_height
        x = x * distance

        vec = Vector2(start.x + (x), start.y + y)

        points.append(vec)
    points.append(end)

    if is_negative:
        for p in points:
            p.x = -p.x
            p.x += distance

    return points


if __name__ == "__main__":
    # !usr/bin/env python
    # catenary calculation, re-written in python - NO Elasticity!!!

    import math
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.optimize import fsolve

    def cat(a):
        # defining catenary function
        # catenary eq (math): a*sinh(L/(2*a)+atanh(d/S))+a*sinh(L/(2*a)-atanh(d/S))-S=0
        return (
            a * math.sinh(L / (2 * a))
            + math.atanh(d / S)
            + a * math.sinh(L / (2 * a))
            - math.atanh(d / S)
            - S
        )

    # L = float(input("Horizontal Distance between supports [m]: "))
    # d = float(input("Vertical Distance between supports [m]: "))
    # S = float(
    #     input("Length of cable [m] - must be greater than distance between supports:  ")
    # )
    # w = float(input("Unit weight of cable [kg/m]: "))
    # za = float(input("Elevation of higher support from reference plane [m]: "))

    L = 32
    d = 12
    S = 40
    w = 8
    za = 12

    # checking if cable length is bigger than total distance between supports
    distance = (L**2 + d**2) ** 0.5
    if S <= distance:
        print("Length of cable must be greater than TOTAL distance between supports!")
        S = float(input("Length of cable [m]: "))
    else:
        pass

    # solving catenary function for 'a'

    a = fsolve(cat, 1)

    # hor. distance between lowest catenary point (P) to higher support point (La)
    La = a[0] * (L / (2 * a[0]) + math.atanh(d / S))
    # hor. distance between lowest catenary point (P) to lower support point (Lb)
    Lb = L - La
    # vert. distance from higher support point to lowest point (P) in catenary (ha)
    ha = a[0] * math.cosh(La / a[0]) - a[0]
    ## calculating reaction forces and angles
    # catenary lenght between support "A" (higher) and "P" - Sa
    Sa = a[0] * math.sinh(La / a[0])
    # catenary lenght between support "B" )lower) and "P" - Sb
    Sb = a[0] * math.sinh(Lb / a[0])
    # horizontal tension - constant through catenary: H
    H = w * a[0]
    # vertical tension at "A"  (Va) and "B" (Vb)
    Va = Sa * w
    Vb = Sb * w
    # tension at "A" (TA) and B (TB)
    TA = (H**2 + Va**2) ** 0.5
    TB = (H**2 + Vb**2) ** 0.5
    # inclination angles from vertical at "A" (ThetA) and B (ThetB)
    ThetA = math.atan(H / Va)
    ThetB = math.atan(H / Vb)
    ThetAd = ThetA * 180 / math.pi
    ThetBd = ThetB * 180 / math.pi
    # establishing A, B and P in coordinate system
    # index "a" corresponding to point "A", "b" to "B"-point and "P" to lowest caten. point
    zb = za - d
    zp = za - ha
    xa = La
    xp = 0
    xb = -Lb

    # graphing catenary curve - matplotlib & writting coordinates in file
    xinc = L / 100
    y = []
    xc = []

    # plotting, finally
    plt.plot(xc, y)
    plt.xlabel("X-distance [m]")
    plt.ylabel("Y-distance [m]")
    plt.grid()
    plt.show()

    input("Press Enter to exit...")
