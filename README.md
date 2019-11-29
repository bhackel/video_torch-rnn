# video_torch-rnn
code used to make this video https://youtu.be/6-Zk9Z3lEK0 on torch-rnn

I made this using pyqt by saving images and making it into a video with ffmpeg, don't recommend
yes those are matplotlib charts

If you want to run this thing, the MYSTUFF and preprocessing folders go in the same directory as all of the parts of torch-rnn.
To make the necessary files to output a video, first need to run create_checkpoints.py to make the around 20GB of checkpoint files.
Next, run train_loss.py to generate the matplotlib images, which will be placed in train_loss/
Finally, run video.py to create the full GUI images, stitch them together, and add some audio.

I used Python 3.5 on Ubuntu 16.04 with ffmpeg installed. The dependencies include a qt binding (pyqt or pyside2), qtpy, matplotlib, and probably some other ones.
