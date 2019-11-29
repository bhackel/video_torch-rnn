import subprocess

#--===****^****===--#

#filename, exclude .txt extension. file is in data directory
filename = 'oregairu-full-mod'

#--===****^****===--#

program = '.env/bin/python'
directory = '../scripts/preprocess.py'

p1 = '--input_txt'
p2 = '../data/' + filename + '.txt'

p3 = '--output_h5'
p4 = '../preprocessing/' + filename + '.h5'

p5 = '--output_json'
p6 = '../preprocessing/' + filename + '.json'


command = [program, directory, p1, p2, p3, p4, p5, p6]

subprocess.call(command)