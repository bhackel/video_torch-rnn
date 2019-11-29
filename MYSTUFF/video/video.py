from qtpy import QtWidgets, QtGui, QtCore
import sys, os, subprocess, datetime

class Label_Header(QtWidgets.QLabel):
    """A subclass of the QLabel class used for the headers"""
    def __init__(self):
        QtWidgets.QLabel.__init__(self)
        font = QtGui.QFont("Arial", 24, QtGui.QFont.Bold)
        self.setFont(font)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setMargin(0)
        self.setFixedHeight(50)
        self.setStyleSheet("QLabel { background-color: #eee }")


class Label_Text(QtWidgets.QLabel):
    """subclass of QLabel  used for sample text and commentary"""
    def __init__(self):
        QtWidgets.QLabel.__init__(self)
        font = QtGui.QFont( "Arial", 16)
        self.setFont(font)
        self.setAlignment(QtCore.Qt.AlignTop)
        self.setMargin(30)
        self.setWordWrap(True)
        self.setStyleSheet("QLabel { background-color: #eee }")


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # stuff that should not be changed
        self.width = 1920
        self.height = 1080

        # relative paths for folders containing various things
        self.img_path = './train_loss/'
        self.out_path = './video_frames/'
        self.checkpoint_path = '../../cv-VIDEO-4x512-lstm-mod/'
        self.commentary_path = './commentary/'

        self.setup()

    def setup(self):
        """
        The part that creates the labels and text boxes and
        image box and then puts it all into a grid that is
        3 rows by 3 columns
        """

        self.grid = QtWidgets.QGridLayout()

        self.l_header_1 = Label_Header()
        self.l_header_2 = Label_Header()
        self.l_header_3 = Label_Header()
        self.l_sample_text = Label_Text()
        self.l_commentary = Label_Text()
        font = QtGui.QFont( "Arial", 24)
        self.l_commentary.setFont(font)
        self.l_loss_image = QtWidgets.QLabel()

        # setting up the label which holds the training loss graph
        self.l_loss_image.setPixmap(QtGui.QPixmap(self.img_path
                                                  +'image0000-000001.png'))
        self.l_loss_image.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                        QtWidgets.QSizePolicy.Fixed );
        self.l_loss_image.setAlignment(QtCore.Qt.AlignCenter)
        self.l_loss_image.setMargin(0)
        self.l_loss_image.setStyleSheet("QLabel { background-color: #fff }")
        
        # adding crud to places in the grid, kinda hard to visualize
        self.grid.addWidget(self.l_header_1, 0, 0, 1, 1)
        self.grid.addWidget(self.l_header_2, 0, 1, 1, 1)
        self.grid.addWidget(self.l_header_3, 0, 2, 1, 1)
        self.grid.addWidget(self.l_sample_text, 1, 0, 1, 2)
        self.grid.addWidget(self.l_commentary, 1, 2, 1, 1)
        self.grid.addWidget(self.l_loss_image, 2, 0, 1, 3)

        # setting spacing between labels, other labels, and border
        #self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)
        
        self.setLayout(self.grid)
        self.setStyleSheet("background-color: #bbb")
        self.resize(self.width, self.height)

        #self.show()

    def save_image(self, image_num=0):
        """
        saves the current instance of the gui into the
        folder specified by out_path
        """
        img = QtWidgets.QWidget.grab(self)
        self.render(img)
        img.save("{}image{:04d}.png"
                 .format(self.out_path, image_num), 'png')

    def get_sample_text(self, checkpoint=1, length=1500):
        """
        Returns sample text based on the given checkpoint and 
        given length of the sample. the command is run in the
        directory containing all the neural network stuff
        """
        result = ""
        path = 'cv-VIDEO-4x512-lstm-mod/'
        file = path + 'checkpoint_' + str(checkpoint) + '.t7'

        p1 = ['th', 'sample.lua']
        p2 = ['-checkpoint', file]
        p3 = ['-length', str(length)]
        args = p1 + p2 + p3
        cwd = '../../'
        try:
            result = subprocess.check_output(args, cwd=cwd)
            result = result.decode("utf-8")
            return result
        except:
            print("sampling broke")

    def get_commentary(self, frame_num=0, sample=False, old=""):
        """
        Returns commentary based on given number. Commentary is in
        folder specified by self.commentary_path
        """
        file_num = str(frame_num) + ("s"*int(sample))
        fname = (self.commentary_path + file_num + ".txt")

        if os.path.isfile(fname):
            with open(fname, 'r') as file:
                commentary = file.read()
        else:
            commentary = old

        return commentary

    def get_closest_checkpoint(self, iter_count, checkpoints):
        """
        Returns the nearest checkpoint, searching only 
        checkpoints below the given iteration number
        """
        approx_checkpoint = 0
        for num in checkpoints:
            if (num > iter_count):
                break
            approx_checkpoint = num
        return approx_checkpoint

    def clean_label_text(self, text, iteration):
        """
        Returns shortened version of text with only 17? line breaks
        so that the labels don't stretch beyond the 1920x1080 window
        """
        text = ("Sample of Iteration {}\n{}\n{}"
                .format(iteration, "─"*41, text))
        line_break_count = text.count("\n")
        # repeatedly shorten by 1 character until is good
        while line_break_count >= 18:
            text = text[0:len(text)-1]
            line_break_count = text.count("\n")
        return text

    def get_estimated_time(self, iter_count):
        seconds_per_iter = (1571637924-1571610915)/(106500-1000)
        estimated_seconds = int(seconds_per_iter*iter_count)
        est_time = datetime.timedelta(seconds=estimated_seconds)
        return est_time

    def create_video_from_images(self):
        # using ffmpeg of course
        print('ffmpeg is now...')

        p1 = ['ffmpeg']
        p2 = ['-r', '30']
        p3 = ['-i', self.out_path+'image%04d.png']
        p4 = ['-c:v', 'libx264']
        p5 = ['-vf', 'fps=30']
        p6 = ['-hide_banner']
        p7 = ['-loglevel', 'panic']
        p8 = ['-y']
        p9 = ['video.avi']

        command = p1+p2+p3+p4+p5+p6+p7+p8+p9

        subprocess.call(command)

    def add_audio_to_video(self):
        print('adding audio to video.avi...')

        p1 = ['ffmpeg']
        p2 = ['-i', 'video.avi']
        p3 = ['-itsoffset', '3']
        p4 = ['-i', 'audio.mp3']
        p5 = ['-c:a', 'ac3']
        p6 = ['-b:a', '192k']
        p7 = ['-c:v', 'libx264']
        p8 = ['-filter:a', "volume=0.05"] 
        p9 = ['-shortest']
        p10 = ['-hide_banner']
        p11 = ['-loglevel', 'panic']
        p12 = ['-y']
        p13 = ['video.mp4']

        command = p1+p2+p3+p4+p5+p6+p7+p8+p9+p10+p11+p12+p13

        subprocess.call(command)

    def video_loop(self):
        """
        the meat of the video creation
        """
        train_loss_images = os.listdir(self.img_path)
        train_loss_images.sort()
        # remove the first image from the list cuz it's used only
        # in the introduction
        start_train_loss_image = train_loss_images.pop(0)
        total_frames = len(train_loss_images)

        checkpoints = os.listdir(self.checkpoint_path)
        checkpoints.remove('checkpoint_runs.txt')
        checkpoints = [os.path.splitext(i)[0] for i in checkpoints]
        checkpoints = [int(i.split('_')[1]) for i in checkpoints]
        checkpoints.sort()

        old_iter_count = 0
        cur_frame = 0
        begin = False

        # new thing, gonna make the start frames here instead
        # of as a part of the main loop
        print("---- starting with starting frames ----")
        total_start_frames = 300 # must be multiple of 150
        for cur_frame in range(0, total_start_frames):
            print("creating start frame {} of {}"
                  .format(cur_frame, total_start_frames-1))

            if cur_frame == 0:
                # set intro commentary and sample text
                intro_sample_text = self.get_commentary(0, True)
                intro_commentary = self.get_commentary(0)
                self.l_sample_text.setText(intro_sample_text)
                self.l_commentary.setText(intro_commentary)

                font = QtGui.QFont( "Arial", 24)
                self.l_sample_text.setFont(font)

                self.l_header_1.setText("「Epochs」")
                self.l_header_2.setText("「Iterations」")
                self.l_header_3.setText("「Estimated Time Elapsed」")

                t_l_file = self.img_path + start_train_loss_image
                t_l_pixmap = QtGui.QPixmap(t_l_file)
                self.l_loss_image.setPixmap(t_l_pixmap)

            self.save_image(image_num=cur_frame)

        font = QtGui.QFont( "Arial", 16)
        self.l_sample_text.setFont(font)
        cur_frame += 1
        commentary = ""

        for train_loss_image in train_loss_images:
            # calculate values for headers
            iter_count = int(train_loss_image[10:16])
            epoch = ((iter_count / 106500) * 50)
            est_time = self.get_estimated_time(iter_count)

            # log current frame
            print("creating frame {} of {}"
                  .format(cur_frame, total_frames+total_start_frames-1)
                  , end="")
            if old_iter_count != iter_count:
                print(" - new loss image")
            else:
                print()
            old_iter_count = iter_count

            # update headers
            self.l_header_1.setText("Epoch {0:.2f} of 50".format(epoch))
            self.l_header_2.setText("Iteration {}".format(iter_count))
            self.l_header_3.setText("Est. Time: {}".format(est_time))

            # update the training loss image
            t_l_file = self.img_path + train_loss_image
            t_l_pixmap = QtGui.QPixmap(t_l_file)
            self.l_loss_image.setPixmap(t_l_pixmap)

            # update the sample text every 150 frames (5 seconds)
            if cur_frame % 150 == 0:
                print(" updating the sample text...")
                
                checkpoint = self.get_closest_checkpoint(iter_count,
                                                         checkpoints)
                sample = self.get_sample_text(checkpoint)
                sample = self.clean_label_text(sample, checkpoint)
                self.l_sample_text.setText(sample)

                commentary = self.get_commentary(cur_frame, old=commentary)
                self.l_commentary.setText(commentary)

            # save the graphic and tick the iterator
            self.save_image(image_num=cur_frame)
            cur_frame += 1

        # final frames to conclude things
        print("---- doing end frames now ----")
        final_frame = cur_frame
        total_end_frames = 600
        final_iter = checkpoints[-1]
        halfway = final_frame + int(total_end_frames//2)

        for cur_frame in range(cur_frame, final_frame+total_end_frames):
            print("creating end frame {} of {}"
                  .format(cur_frame, final_frame+total_end_frames-1))

            if cur_frame == final_frame:
                # show the ending commentary and final results
                sample = self.get_sample_text(checkpoint=final_iter)
                sample = self.clean_label_text(sample, final_iter)
                outro_commentary = self.get_commentary(-1)
                self.l_sample_text.setText(sample)
                self.l_commentary.setText(outro_commentary)

                est_time = self.get_estimated_time(final_iter)
                self.l_header_1.setText("Epoch 50 of 50")
                self.l_header_2.setText("Iteration {}".format(final_iter))
                self.l_header_3.setText("Est. Time: {}".format(est_time))

            elif cur_frame == halfway:
                # halfway, change to second ending commentary,
                # and get new sample text
                sample = self.get_sample_text(checkpoint=final_iter)
                sample = self.clean_label_text(sample, final_iter)
                self.l_sample_text.setText(sample)

            self.save_image(image_num=cur_frame)

            


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.video_loop()
    win.create_video_from_images()
    win.add_audio_to_video()
    sys.exit()

if __name__ == '__main__':
    main()