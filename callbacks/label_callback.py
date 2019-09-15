import pandas as pd
from callbacks.image_callback import ImageUpdaterCallback


class ImageLabelingCallback:

    def __init__(self, image_callback: ImageUpdaterCallback, label_dict, mode, label='Symbol', savefile='labels.csv'):
        self.image_callback: ImageUpdaterCallback = image_callback
        self.label_dict = label_dict
        self.mode = mode
        self.label = label
        self.savefile = savefile
        if 'skip_' in mode:
            self.ignore_label = mode.split('skip_')[-1]
            print('Skip mode for label', self.ignore_label)
            self.next_cb = self._skip_matching
            self.next_cb()
        elif 'skip' in mode:
            print('Skipping all seen images')
            self.next_cb = self._skip_seen
            self.next_cb()
        else:
            print('Starting from clean slate')
            self.next_cb = self._noskip

    def _skip_seen(self, *args, **kwargs):
        idx = self.image_callback.idx
        image_path = self.image_callback.files[idx]
        while image_path in self.label_dict['image_path']:
            self.image_callback(*args, **kwargs)
            if self.image_callback.idx == 0:
                break

    def _skip_matching(self, *args, **kwargs):
        idx = self.image_callback.idx
        image_path = self.image_callback.files[idx]
        while (image_path in self.label_dict['image_path']):
            self.image_callback(*args, **kwargs)
            idx = self.image_callback.idx
            if not (self.label_dict['label'][idx] == self.ignore_label):
                break
            if self.image_callback.idx == 0:
                break


    def _noskip(self, *args, **kwargs):
        self.image_callback(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        path = (self.image_callback.files[self.image_callback.idx])
        label = self.label
        idx = self.image_callback.idx
        if path in self.label_dict['image_path']:
            idx = self.label_dict['image_path'].index(path)
            self.label_dict['label'][idx] = label
        else:
            self.label_dict['image_path'].append(path)
            self.label_dict['label'].append(label)
            self.label_dict['index'].append(idx)
        self.next_cb(*args, **kwargs)
        pd.DataFrame.from_dict(self.label_dict).to_csv(self.savefile, sep=';', index_label='index')
        if self.image_callback.idx == 0:
            exit(0)
        return
