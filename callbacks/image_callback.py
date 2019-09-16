from os import listdir
from os.path import join
from copy import deepcopy
from PIL import Image, ImageTk

class ImageUpdaterCallback:

    def _get_files(self, root):
        filenames = [join(root, file) for file in listdir(root)]
        return filenames

    def __init__(self, root_path, panel, input_resolution, root):
        self.root_path = root_path
        self.input_resolution = input_resolution
        self.files = self._get_files(self.root_path)
        self.num_files = len(self.files)
        self.full_length_files = deepcopy(self.files)
        self.panel = panel
        self.idx = 0
        self.root = root

    def __call__(self, *args, **kwargs):
        self.root.config(text="{} of {} Images processed".format(1+self.full_length_files.index(self.files[self.idx]), len(self.full_length_files)))
        self.idx += 1
        if self.idx >= len(self.files):
            self.idx = 0
        img = Image.open(self.files[self.idx])
        img.thumbnail(self.input_resolution, Image.ANTIALIAS)
        new_img = ImageTk.PhotoImage(img)
        self.panel.configure(image=new_img)
        self.panel.image = new_img


class MoverCallback:

    def __init__(self, image_cb: ImageUpdaterCallback, left_or_right):
        self.img_cb = image_cb
        self.left_or_right = left_or_right
        pass

    def __call__(self, *args, **kwargs):
        if self.left_or_right == 'left':
            self.img_cb.idx -= 1
        elif self.left_or_right == 'right':
            self.img_cb.idx += 1

        if self.img_cb.idx >= len(self.img_cb.files):
            self.img_cb.idx = 0
        if self.img_cb.idx < 0:
            self.img_cb.idx = len(self.img_cb.files)-1
        img = Image.open(self.img_cb.files[self.img_cb.idx])
        img.thumbnail(self.img_cb.input_resolution, Image.ANTIALIAS)
        new_img = ImageTk.PhotoImage(img)
        self.img_cb.panel.configure(image=new_img)
        self.img_cb.panel.image = new_img

