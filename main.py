import tkinter as tk
import argparse
import pandas as pd
from os import listdir
from PIL import ImageTk
from PIL import Image
from os.path import join, exists
from callbacks.image_callback import ImageUpdaterCallback, MoverCallback
from callbacks.label_callback import ImageLabelingCallback


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', default='labeled.csv', dest='output')
    parser.add_argument('-m', '--mode', default='skip_no_symbol', dest='mode')
    parser.add_argument('-i', '--input', default=join('.', 'imgs'), dest='input')
    args = parser.parse_args()

    input_resolution = (1000, 1000)

    root = tk.Tk()
    path = args.input #join('.', 'imgs', 'test.jpg')
    img = Image.open(join(path, listdir(path)[-1]))
    img.thumbnail(input_resolution, Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)

    panel = tk.Label(root, image=img)

    panel.pack(side=tk.BOTTOM, fill="both", expand="yes")
    display = tk.Label(root, text="TEST123")
    callback = ImageUpdaterCallback(args.input, panel, input_resolution, display)
    if not exists(args.output):
        label_dict = {
            'image_path': [],
            'label': [],
            'index': []
        }
    else:
        label_dict = pd.read_csv(args.output, sep=';', index_col='index').to_dict('list')
        label_dict['index'] = label_dict.pop('index.1', None)

    symbol_callback = ImageLabelingCallback(image_callback=callback, label_dict=label_dict, label='remove', mode=args.mode, savefile=args.output)
    no_symbol_callback = ImageLabelingCallback(image_callback=callback, label_dict=label_dict, label='keep', mode=args.mode, savefile=args.output)
    b_true = tk.Button(root, compound='left', text="Keep (N)", command=no_symbol_callback)
    b_false = tk.Button(root, compound='right', text="Remove (Y)", command=symbol_callback)
    b_true.pack(side=tk.LEFT)
    b_false.pack(side=tk.RIGHT)
    display.pack(side=tk.BOTTOM)

    left_cb = MoverCallback(image_cb=callback, left_or_right='left')
    right_cb = MoverCallback(image_cb=callback, left_or_right='right')


    root.title("Simple Labeler 1.0")
    root.bind("<Return>", lambda e: exit(0))
    root.bind('y', symbol_callback)
    root.bind('n', no_symbol_callback)
    root.bind('<Left>', left_cb)
    root.bind('<Right>', right_cb)
    root.mainloop()