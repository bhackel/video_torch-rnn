import subprocess

'''
th sample.lua
-checkpoint cv/checkpoint_1065000.t7
-length 100000
'''

checkpoint = 106500
length = 100000

result = ""
path = 'cv-VIDEO-4x512-lstm-mod/'
file = path + 'checkpoint_' + str(checkpoint) + '.t7'

p1 = ['th', 'sample.lua']
p2 = ['-checkpoint', file]
p3 = ['-length', str(length)]
args = p1 + p2 + p3
cwd = '../../'

result = subprocess.check_output(args, cwd=cwd)
result = result.decode("utf-8")

with open('long_sample', 'w') as f:
	f.write(result)