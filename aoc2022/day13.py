
from copy import deepcopy
from itertools import compress
from functools import reduce
import operator
from collections import defaultdict

lines = [x.rstrip("\n\r") for x in open("input13.txt", "r")]