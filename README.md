# PieKick
evaluate functions on a remote machine with a single decorator.

## example
this code snippet executes locally. 
```python
def foobar():
    res = 0
    for i in range(3):
        res += i
    print(res)

foobar()  # foobar() evaluated on local machine and prints 3
```

we can evaluate `foobar()` on a remote machine (eg ec2) with a single decorator `@kick`. no `ssh`, `scp`, or moving bytes back and forth.
```python
from kick import kick

@kick
def foobar():
    res = 0
    for i in range(3):
        res += i
    print(res)

foobar()  # foobar() remote execution
```