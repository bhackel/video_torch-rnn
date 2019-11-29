import subprocess
import math

# This file should be in the MYSTUFF subfolder of Torch-RNN
# The resulting checkpoints will be placed in the checkpoint_name
# subfolder of Torch-RNN folder
# It will run for a while...

# 50 epochs did 106500 iterations
# 1 epoch does 2130 iterations
# 1 iteration is 0.000469483568 epochs

def round(number):
	# rounds up the given number
	precision = 1000000
	return math.ceil(number*precision)/precision

cwd = '../'
checkpoint_name = 'cv-VIDEO-4x512-lstm-mod/checkpoint'
checkpoint_every = 1
max_epochs = round((1/106500) * 50)
checkpoint_num = 1

'''
th train.lua
-input_h5 preprocessing/oregairu-full-mod.h5
-input_json preprocessing/oregairu-full-mod.json
-model_type lstm
-num_layers 4
-rnn_size 512
-max_epochs 50
-checkpoint_name cv-chk1-4x512-lstm-mod/checkpoint
-checkpoint_every 1
-max_epochs 0.025
'''

p1 = ['th', 'train.lua']
p2 = ['-input_h5', 'preprocessing/oregairu-full-mod.h5']
p3 = ['-input_json', 'preprocessing/oregairu-full-mod.json']
p4 = ['-checkpoint_every', str(checkpoint_every)]
p5 = ['-max_epochs', str(max_epochs)]
p6 = ['-checkpoint_name', str(checkpoint_name)]
p7 = ['-rnn_size', '512']
p8 = ['-num_layers', '4']
p9 = ['-model_type', 'lstm']

command = p1+p2+p3+p4+p5+p6+p7+p8

print("----- creating first checkpoint -----")
subprocess.call(command, cwd=cwd)



# now that the first checkpoint is created, we shall continue
p10 = ['-reset_iterations', '0']

# tuples are (checkpoint_every by max_iteration)
runs = [(1, 50), (2, 100), (10, 500), (100, 5000), (500, 53250), (1000, 106500)]
with open(cwd+checkpoint_name+'_runs.txt', 'w') as f:
	# write the final checkpoints to a file for later use
	content = "\n".join([str(i[1]) for i in runs])
	f.write(content)


for pair in runs:
	# unpack
	checkpoint_every, max_iteration = pair
	max_epochs = round((max_iteration/106500) * 50)
	print("----- beginning iterations {} to {} by {} -----"
		  .format(checkpoint_num, max_iteration, checkpoint_every))


	# update lists
	p4 = ['-checkpoint_every', str(checkpoint_every)]
	p5 = ['-max_epochs', str(max_epochs)]
	p11 = ['-init_from', checkpoint_name+'_'+str(checkpoint_num)+'.t7']

	# compile the command
	command = p1+p2+p3+p4+p5+p6+p7+p8+p9+p10+p11

	# call it
	subprocess.call(command, cwd=cwd)

	# setup for next run
	checkpoint_num = max_iteration
