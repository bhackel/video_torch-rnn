import json
import matplotlib.pyplot as plt
import subprocess, math, os

# inefficiency is the name of this game

checkpoint_path = '../../cv-VIDEO-4x512-lstm-mod/'
runs_file = checkpoint_path + 'checkpoint_runs.txt'

# open file with runs used
with open(runs_file) as f:
    runs = f.read().splitlines()
runs.insert(0,1)

# compile all train loss values from the final checkpoint json files
train_losses = []
for run in runs:
    checkpoint_file = checkpoint_path+'checkpoint_'+str(run)+'.json'
    with open(checkpoint_file) as f:
        data = f.read()
    data = json.loads(data)
    train_losses += data['train_loss_history']
    

image_index = 0
train_index = 1
update_amt = 1
width = 1920
height = 360
dpi = 96

# arbitrary
def get_num_images(iteration):
    result = math.ceil(300/iteration)
    '''b = 1.01919449879
    result = -math.log(iteration, b)'''
    
    if result < 1:
        result = 1
    return result

# arbitrary
def get_update_amt(iteration):
    result = math.ceil(iteration/500)
    '''b = 1.00003
    h = -72641.9
    k = -7
    result = int(b ** (iteration - h)) + k'''

    '''a = 1/10000000
    result = int(a*(iteration**2))+1'''
    
    if result < 1:
        result = 1
    return result



print('generating images now...')
while train_index <= len(train_losses):
    num_images = get_num_images(train_index)
    
    # setup and create a matplotlib chart, ehh dont feel like commenting...
    fig, ax = plt.subplots(figsize=(width/dpi, height/dpi))
    ax.plot([train_losses[0]] + train_losses[0:train_index])
    ax.set(xlabel='iterations', ylabel='train loss')

    for i in range(num_images):
        print('creating image {} of index {} for frame {}'
              .format(i, train_index, image_index))
        fig.savefig('train_loss/image{:04d}-{:06d}.png'
                    .format(image_index, train_index), dpi=dpi)
        image_index += 1

    if train_index == 1:
        print('creating 0-0 image')
        plt.close()
        fig, ax = plt.subplots(figsize=(width/dpi, height/dpi))
        ax.plot([train_losses[0]])
        ax.set(xlabel='iterations', ylabel='train loss')
        fig.savefig('train_loss/image0000-000000.png', dpi=dpi)


    plt.close()

    update_amt = get_update_amt(train_index)
    train_index += update_amt

train_index = len(train_losses)
print('creating final image, index {}'.format(train_index))

fig, ax = plt.subplots(figsize=(width/dpi, height/dpi))
ax.plot([train_losses[0]] + train_losses)
ax.set(xlabel='iterations', ylabel='train loss')
fig.savefig('train_loss/image{:04d}-{:06d}.png'
            .format(image_index, train_index), dpi=dpi)
plt.close()


#--===****^****===--#
'''
print('ffmpeg is now...')

p1 = ['ffmpeg']
p2 = ['-r', '30']
p3 = ['-i', 'train_loss/image%04d.png']
p4 = ['-c:v', 'libx264']
p5 = ['-vf', 'fps=30']
p6 = ['-hide_banner']
p7 = ['-loglevel', 'panic']
p8 = ['train_losses.avi']

command = p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8

subprocess.call(command)'''