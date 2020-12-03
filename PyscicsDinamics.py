class Vector(list):
    def __init__(self, *el):
        for e in el:
            self.append(e)

    def __add__(self, other):
        if type(other) is Vector:
            assert len(self) == len(other), "Error 0"
            r = Vector()
            for i in range(len(self)):
                r.append(self[i] + other[i])
            return r
        else:
            other = Vector.emptyvec(lens=len(self), n=other)
            return self + other

    def __sub__(self, other):
        if type(other) is Vector:
            assert len(self) == len(other), "Error 0"
            r = Vector()
            for i in range(len(self)):
                r.append(self[i] - other[i])
            return r
        else:
            other = Vector.emptyvec(lens=len(self), n=other)
            return self - other

    def __mul__(self, other):
        if type(other) is Vector:
            assert len(self) == len(other), "Error 0"
            r = Vector()
            for i in range(len(self)):
                r.append(self[i] * other[i])
            return r
        else:
            other = Vector.emptyvec(lens=len(self), n=other)
            return self * other

    def __truediv__(self, other):
        if type(other) is Vector:
            assert len(self) == len(other), "Error 0"
            r = Vector()
            for i in range(len(self)):
                r.append(self[i] / other[i])
            return r
        else:
            other = Vector.emptyvec(lens=len(self), n=other)
            return self / other

    def __pow__(self, other):
        if type(other) is Vector:
            assert len(self) == len(other), "Error 0"
            r = Vector()
            for i in range(len(self)):
                r.append(self[i] ** other[i])
            return r
        else:
            other = Vector.emptyvec(lens=len(self), n=other)
            return self ** other

    def __mod__(self, other):
        return sum((self - other) ** 2) ** 0.5

    def mod(self):
        return self % Vector.emptyvec(len(self))

    def dim(self):
        return len(self)
    
    def __str__(self):
        if len(self) == 0:
            return "Empty"
        r = [str(i) for i in self]
        return "< " + " ".join(r) + " >"
    
    def _ipython_display_(self):
        print(str(self))

    @staticmethod
    def emptyvec(lens=2, n=0):
        return Vector(*[n for i in range(lens)])

class Point:
    def __init__(self, coords, mass, q, speed=None, **properties):
        self.coords = coords
        if speed is None:
            self.speed = Vector(*[0 for i in range(len(coords))])
        else:
            self.speed = speed
        self.acc = Vector(*[0 for i in range(len(coords))])
        self.mass = mass
        self.__params__ = ["coords", "speed", "acc", "q"] + list(properties.keys())
        self.q = q
        for prop in properties:
            setattr(self, prop, properties[prop])

    def move(self, dt):
        self.coords = self.coords + self.speed * dt

    def accelerate(self, dt):
        self.speed = self.speed + self.acc * dt

    def accinc(self, force):
        self.acc = self.acc + force / self.mass
    
    def clean_acc(self):
        self.acc = self.acc * 0
    
    def __str__(self):
        r = ["Point {"]
        for p in self.__params__:
            r.append("  " + p + " = " + str(getattr(self, p)))
        r += ["}"]
        return "\n".join(r)

    def _ipython_display_(self):
        print(str(self))


class InteractionField:
    def __init__(self, F):
        self.points = []
        self.F = F

    def move_all(self, dt):
        for p in self.points:
            p.move(dt)

    def intensity(self, coord):
        proj = Vector(*[0 for i in range(coord.dim())])
        single_point = Point(Vector(), mass=1.0, q=1.0)
        for p in self.points:
            if coord % p.coords < 10 ** (-10):
                continue
            d = p.coords % coord
            fmod = self.F(single_point, p, d) * (-1)
            proj = proj + (coord - p.coords) / d * fmod
        return proj

    def step(self, dt):
        self.clean_acc()
        for p in self.points:
            p.accinc(self.intensity(p.coords) * p.q)
            p.accelerate(dt)
            p.move(dt)

    def clean_acc(self):
        for p in self.points:
            p.clean_acc()
    
    def append(self, *args, **kwargs):
        self.points.append(Point(*args, **kwargs))
    
    def gather_coords(self):
        return [p.coords for p in self.points]
 
class constants:
    G = 6.67138e-11
    GeoMass = 5.691e+22
    pass
