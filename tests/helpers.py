import os, sys

TEST_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)))

# Add project to import path
sys.path.append(str(os.path.join(TEST_ROOT, "..")))
