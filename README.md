## CLIPS Web App

- Provides a web app as a user interface to CLIPS source files
- Tested on Ubuntu 16.04 and 18.04 LTS
- Works with both Python 2 and 3 as they are supported by the CLIPS integration library ([clipspy](https://clipspy.readthedocs.io/en/latest/index.html) which is imported as `clips` and installed through pip)

### To install
```
$ pip install -r requirements.txt
```

### To run
```
$ python app.py
```

### To update new CLIPS source
1. Put it in the same folder and replace the CLIPS I/O functions with the equivalent standardised placeholders (can refer to the changes in the examples and `header_clips.clp`)
2. Visit the link http://127.0.0.1:5000/<new clips filename without .clp extension>

### CLIPS source code
The modified `*.clp` files are incomplete by themselves (unlike the originals). To run in CLIPS, prepend the contents of `header_clips.clp` first. To run in Python like the example Jupyter notebook, write the Python functions first, then `define_function` with clipspy, then load your CLIPS source.

### Credits
CLIPS example scripts modified from:
- https://github.com/smarr/CLIPS/blob/master/examples/animal.clp
- https://github.com/smarr/CLIPS/blob/master/examples/auto.clp

Photos from:
- https://www.pexels.com/photo/photography-of-maple-trees-1114896/
- https://www.pexels.com/photo/alley-autumn-autumn-colours-autumn-leaves-235721/
