# This Python file allows for simple checking of the build proceedure
# without invoking FrameMaker 

# It starts by regurgitating the input parameters

import sys

print ("Build Test")

print ("Python version:", sys.version)

if __name__ == "__main__":
    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>6}: {arg}")