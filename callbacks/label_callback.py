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
            self._remove_matching(self.label_dict, self.image_callback.files)
        elif 'skip' in mode:
            print('Skipping all seen images')
            self._remove_seen(self.label_dict, self.image_callback.files)
        else:
            print('Starting from clean slate')
        self.next_cb = self._noskip

    def _remove_seen(self, result_dict: dict, filelist: list):
        for i, path in enumerate(result_dict['image_path']):
            if path in filelist:
                filelist.remove(path)
        return filelist

    def _remove_matching(self, result_dict: dict, filelist: list):
        for i, path in enumerate(result_dict['image_path']):
            if path in filelist and result_dict['label'][i] == self.ignore_label:
                filelist.remove(path)
        return filelist

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
