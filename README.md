Interval arithmetic in Python using Algebraic Data Types
More or less based on [a Haskell package](https://hackage.haskell.org/package/intervals-0.8.1/docs/Numeric-Interval.html)

Requires uxadt

```bash
sudo pip3 install -r requirements.txt
```

Supports arithmetic (add,sub,mul,div) and comparison. 
Comparison using forall by default.
Use e.g., ltSome or leSome if x < y for some values of x and y
Equality is weird for intervals.

Addition:
```python3
>>>Interval(-1,3) + Interval(4,5)
Interval(3,8)
>>>Interval(1,3) + Empty()
Empty()
>>>Empty() + Interval(1,3)
Empty()
```

Multiplication:
```python3
>>>Interval(-1,3) * Interval(4,5)
Interval(-5,15)
>>>Interval(-3,3) * Interval(-5,2)
Interval(-15,15)
>>>Interval(1,3) * Empty()
Empty()
>>>Empty() * Interval(1,3)
Empty()
```

Unary minus operator
```python3
>>>-Interval(-1,3)
Interval(-3,1)
>>>-Empty()
Empty()
```

Binary minus operator
```python3
>>>Interval(3,6) - Interval(-4,2)
Interval(1,10)
>>>Empty() - Interval(1,2)
Empty()
```

Division
```python3
>>>Interval(1,3) / Interval(3,5)
Interval(0.2,1.0))
>>>Interval(1,3) / Interval(-1,1)
Interval(-inf,inf)
>>>Interval(1,3) / Interval(0,3)
Interval(0.3333333333333333, inf)
```

Inclusion
```python3
>>>1 in Interval(0,2)
True
>>>-1 in Interval(0,2)
False
>>>1 in Empty()
False
```
