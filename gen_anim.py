import json
import sys
import math

import numpy as np

def main(output_json):
    o = []
    for i in range(1, 129):
        d = {
            'frame': i,
            'objects':{
                'palm_0': (math.sin(i), math.cos(i), 0),
            }
        }
        o.append(d)
    
    with open(output_json, 'wt') as f:
        json.dump(o, f, indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <output_json>")
    main(*sys.argv[1:])