import os
import sys

for m in sys.modules.keys():
    if m.startswith("park_api"):
        raise Exception("Include helpers module before any park_api module")
os.environ["env"] = "testing"

TEST_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)))

# Add project to import path
sys.path.append(str(os.path.join(TEST_ROOT, "..")))
