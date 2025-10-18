import subprocess
import sys
import re
import os

PY = sys.executable
SIM = os.path.join(os.path.dirname(__file__), 'simulator.py')

common_args = [
    '--a_multi', '1',
    '--cube', '50',
    '--mx_off', '3600',
    '--mxh_off', '86400',
    '--mxv_off', '86400',
    '--mx_off2', '3600',
    '--mxh_off2', '86400',
    '--mxv_off2', '86400',
    '--rs', '0',
    '--hs', '0',
    '--vs', '0',
    '--step', '1',
    '--time_step', '0'
]

# Run range 30->50
range_args = common_args + ['--forStart', '30', '--maxTe', '50']
print('Running range 30->50...')
subprocess.check_call([PY, SIM] + range_args)
# The simulator writes a file named like "{forStart}_to_{maxTe} - {forStep} - {mx_off} - {int(a_multi)}.txt"
range_file = '30_to_50 - 1 - 3600 - 1.txt' if os.path.exists('30_to_50 - 1 - 3600 - 1.txt') else '30_to_50 - 1 - 600 - 179.txt'

# Run single TE=32
single_args = common_args + ['--forStart', '32', '--maxTe', '32']
print('Running single 32...')
subprocess.check_call([PY, SIM] + single_args)
single_file = '32_to_32 - 1 - 3600 - 1.txt' if os.path.exists('32_to_32 - 1 - 3600 - 1.txt') else '32_to_32 - 1 - 600 - 179.txt'

pattern = re.compile(r"([\d\.]+\w*) laying with 32TE")

def extract_te32(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    m = pattern.search(text)
    return m.group(1) if m else None

r = extract_te32(range_file)
s = extract_te32(single_file)
print('range TE32:', r)
print('single TE32:', s)
if r != s:
    print('REGRESSION: values differ')
    sys.exit(2)
print('OK: values match')
