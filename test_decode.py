import re

out = "S000001100000000000000011000000000000000000011000000000001100000000000000000000000000000110000000000S"
out = out.replace("0011", "SS")
print out

decoded = re.findall('S(.*?)S', out)
print decoded
