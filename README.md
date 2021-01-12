# Kick
Remote code execution with decorators.

## Install
Clone this repo and then do `python setup.py install`.
```bash
git clone https://github.com/mynameisvinn/Kick
cd Kick
python setup.py install  # puts kick.ini in home folder
```

## Example
This code snippet executes locally. 
```python
def foobar():
    res = 0
    for i in range(3):
        res += i
    print(res)

foobar()  # foobar() evaluated on local machine and prints 3
```

We can evaluate `foobar()` on a remote machine (eg ec2) with a single decorator `@kick`. no `ssh`, `scp`, or moving bytes back and forth.
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
More examples can be found [here](https://github.com/mynameisvinn/Kick/tree/master/examples)