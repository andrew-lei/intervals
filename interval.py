import uxadt
from functools import partial

class Infix(object):
    def __init__(self, func):
        self.func = func
    def __or__(self, other):
        return self.func(other)
    def __ror__(self, other):
        return Infix(partial(self.func, other))
    def __call__(self, v1, v2):
        return self.func(v1, v2)

_ = None
uxadt._(
    {'Interval': [_,_]
    ,'Empty': []
    })

@Infix
def then(x,f):
    return x._(Interval(_,_), f)\
            ._(Empty(), Empty)\
            .end

# Because == will be used with forall
# 'is' doesn't work and can't be overloaded
@Infix
def match(x,y):
    return x._(Interval(_,_), lambda a,b: 
               y._(Interval(_,_), lambda c,d: a == c and b == d)
                ._(Empty(), lambda: False)
                .end
           )._(Empty(), lambda:
               y._(Empty(), lambda: True)
                ._(Interval(_,_), lambda a,b: False)
                .end
           ).end

def empty(x):
    return x._(Interval(_), lambda _: False)\
            ._(Empty(), lambda: True)\
            .end

def binOp(f):
    return (lambda x, y: 
        x |then| (lambda a,b:
        y |then| f(a,b)))

def forAll(f):
    g = binOp(f)
    return lambda x,y: empty(x) or empty(y) or g(x,y)

def notAll(f): return lambda x,y: not f(x,y) 

# Safe construction
def mkInterval(a,b): return Interval(a,b) if a <= b else Empty()
# +
def addPair(a,b): return lambda c,d: Interval(a+c,b+d)
# *
def multPair(a,b): return lambda c,d: Interval(min(a*c,a*d,b*c,b*d),max(a*c,a*d,b*c,b*d))
# Unary -
def negPair(a,b): return Interval(-b,-a)
# 1/
def invPair(a,b):
    if a*b > 0: return Interval(1/b,1/a)
    return {(False, False): lambda: Interval(float('-inf'),float('inf'))
           ,(False, True): lambda: Interval(float('-inf'), 1/a)
           ,(True, False): lambda: Interval(1/b, float('inf'))
           ,(True, True): Empty
           }[(a==0,b==0)]()
# x /\ y    
def intPair(a,b): return lambda c,d: mkInterval(max(a,c),min(b,d))
# convex hull
def hullPair(a,b): return lambda c,d: Interval(min(a,c),max(b,d))

# b in (a,c)
def containsPair(b): return lambda a,c: a <= b <= c
# < for all
def ltPair(a,b): return lambda c,d: b < c
# <= for all
def lePair(a,b): return lambda c,d: b <= c
# > for all
def gtPair(a,b): return lambda c,d: a > d
# >= for all
def gePair(a,b): return lambda c,d: a >= d
# != for all
def nePair(a,b): return lambda c,d: b < c or a > d
# == for all, True only for singleton and Empty
def eqPair(a,b): return lambda c,d: a == d and b == c

uxadt.uxadt.Value.__add__ = binOp(addPair)
uxadt.uxadt.Value.__mul__ = binOp(multPair)
uxadt.uxadt.Value.__neg__ = lambda x: x |then| negPair
uxadt.uxadt.Value.__sub__ = lambda x,y: x + (-y) 
inv = lambda x: x |then| invPair
uxadt.uxadt.Value.__truediv__ = lambda x,y: x * inv(y)
uxadt.uxadt.Value.__contains__ = lambda x,a: not empty(x) and (x |then| containsPair(a))
intersect = binOp(intPair)
hull = binOp(hullPair)

lt = forAll(ltPair)
le = forAll(lePair)
gt = forAll(gtPair)
ge = forAll(gePair)
eq = forAll(eqPair)
ne = forAll(nePair)
uxadt.uxadt.Value.__lt__ = lt
uxadt.uxadt.Value.__le__ = le
uxadt.uxadt.Value.__gt__ = gt
uxadt.uxadt.Value.__ge__ = ge
uxadt.uxadt.Value.__eq__ = eq
uxadt.uxadt.Value.__ne__ = ne
ltSome = notAll(ge)
leSome = notAll(gt)
gtSome = notAll(le)
geSome = notAll(lt)
neSome = notAll(eq)
eqSome = notAll(ne)

uxadt.uxadt.Value.__is__ = match


if __name__ == '__main__':
    # + 
    assert((Interval(-1,3) + Interval(4,5)) |match| Interval(3,8))
    assert(empty(Interval(1,3) + Empty()))
    assert(empty(Empty() + Interval(1,3)))

    # *
    assert((Interval(-1,3) * Interval(4,5) |match| Interval(-5,15)))
    assert((Interval(-3,3) * Interval(-5,2) |match| Interval(-15,15)))
    assert(empty(Interval(1,3) * Empty()))
    assert(empty(Empty() * Interval(1,3)))

    # Unary -
    assert((-Interval(-1,3)) |match| Interval(-3,1))
    assert(empty(-Empty()))

    # Binary -
    assert((Interval(3,6) - Interval(-4,2)) |match| Interval(1,10))
    assert(empty(Empty() - Interval(1,2)))

    # /
    assert((Interval(1,3) / Interval(3,5)) |match| Interval(1/5,3/3))
    assert((Interval(1,3) / Interval(-1,1)) |match| Interval(float('-inf'),float('inf')))
    assert(empty(Empty() / Interval(-1,1)))

    # in
    assert(1 in Interval(0,2))
    assert(-1 not in Interval(0,2))

    # mkInterval
    assert(mkInterval(1,2) |match| Interval(1,2))
    assert(mkInterval(1,1) |match| Interval(1,1))
    assert(empty(mkInterval(2,1)))

    assert(1 in Interval(0,2))
    assert(Interval(0,2) <= Interval(2,3))
    assert(Empty() >= Interval(1,3))
    assert(ltSome(Interval(1,3),Interval(2,2.5)))
    assert(not Interval(1,3) < Interval(2,2.5))


