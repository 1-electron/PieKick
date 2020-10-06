import inspect
import os
import ast

from .client import up



def kick_web(func):

    # grab context from calling jupyter notebook
    prev_frame = inspect.currentframe().f_back  # previous frame is the notebook
    callers_objects = inspect.getmembers(prev_frame)  # grab all objects from caller's global env
    env = callers_objects[27][1]  # this slice refers to global env from jupyter notebook
    cells =  env['_ih']  # all executed cells up to function call
    print(">> initialize")
    
    def modified_func(*args):

        # step 1: write cell entries to a single file, which will be sent to server
        fname = "temp.py"
        _copy(fname, cells)

        # step 2: create requirements file so server can pip install necessary packages
        _create_requirements(fname)
        
        # step 2: identify calling method
        _append(cells, fname)
        
        # step 3: send source code to remote server
        res = up(fname)  # server's endpoints are found in config properties file

        # step 4: delete temp file
        os.remove("temp.py")

        # step 5: return result
        return res

    return modified_func


def _create_requirements(fname):
    """generate requirements.txt from source code.
    """
    with open(fname) as f: 
        source = f.read()
    
    # create parse tree
    tree = ast.parse(source)
    f = open("requirements.txt", "w")

    # look for ast nodes corresponding to import
    for statement in tree.body:
        if isinstance(statement, ast.Import):
            f.write(statement.names[0].name + "\n")
    f.close()


def _append(cells, fname):
    """modify source code. 
    """
    caller = cells[-1]  # last cell contains method call
    f = open(fname, "a")  # a for append, w for overwrite
    scope = 'res = ' + caller  # res tells server where to save results
    f.write(scope)
    f.close()


def _copy(fname, cells):
    """copy code from notebook cells to a file.
    """
    f = open(fname, "w")

    # iterate through each cell...    
    for cell in cells[:-1]:  # the last one is the calling cell, to be ignored for now
        
        # inside each cell, iterate through each line...
        lines = cell.split("\n")
        for line in lines:
            if ("@kick" in line):
                pass
            elif "Kick" in line:
                pass
            else:
                f.write(line + "\n")
        f.write("\n")
    f.close()