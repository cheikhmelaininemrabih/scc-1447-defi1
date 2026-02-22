import sys
from instance import RCPSPInstance

# Test parsing
inst = RCPSPInstance("/home/cheikhmelainine/SupNum_Challenge_S3C_1447/data/j6010_8.sm")
print("Parsed:", inst)
if inst.check_validity():
    print("Instance Valid!")
else:
    print("Instance INVALID!")
