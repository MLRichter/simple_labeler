from os import listdir
from os.path import join
from PIL import Image, ImageTk

class ImageUpdaterCallback:

    def _get_files(self, root):
        filenames = [join(root, file) for file in listdir(root)]
        return filenames

    def __init__(self, root_path, panel):
        self.root_path = root_path
        self.files = self._get_files(self.root_path)
        self.panel = panel
        self.idx = 0

    def __call__(self, *args, **kwargs):
        self.idx += 1
        if self.idx >= len(self.files):
            self.idx = 0
        new_img = ImageTk.PhotoImage(Image.open(self.files[self.idx]))
        self.panel.configure(image=new_img)
        self.panel.image = new_img
