import tkinter as tk
import argparse
import pandas as pd
from PIL import ImageTk
from PIL import Image
from os.path import join, exists
from callbacks.image_callback import ImageUpdaterCallback
from callbacks.label_callback import ImageLabelingCallback


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', default='labeled.csv', dest='output')
    parser.add_argument('-m', '--mode', default='skip', dest='mode')
    args = parser.parse_args()

    root = tk.Tk()
    path = join('.', 'imgs', 'test.jpg')
    img = ImageTk.PhotoImage(Image.open(path))

    panel = tk.Label(root, image=img)

    panel.pack(side=tk.BOTTOM, fill="both", expand="yes")
    callback = ImageUpdaterCallback(join('.', 'imgs'), panel)
    if not exists(args.output):
        label_dict = {
            'image_path': [],
            'label': [],
            'index': []
        }
    else:
        label_dict = pd.read_csv(args.output, sep=';', index_col='index').to_dict('list')
        label_dict['index'] = label_dict.pop('index.1', None)

    symbol_callback = ImageLabelingCallback(image_callback=callback, label_dict=label_dict, label='symbol', mode=args.mode, savefile=args.output)
    no_symbol_callback = ImageLabelingCallback(image_callback=callback, label_dict=label_dict, label='no_symbol', mode=args.mode, savefile=args.output)
    b_true = tk.Button(root, compound='left', text="No Symbol", command=no_symbol_callback)
    b_false = tk.Button(root, compound='right', text="Symbol", command=symbol_callback)
    b_true.pack(side=tk.LEFT)
    b_false.pack(side=tk.RIGHT)


    root.title("Simple Labeler 1.0")
    root.bind("<Return>", lambda e: exit(0))
    root.bind('y', symbol_callback)
    root.bind('n', no_symbol_callback)
    root.mainloop()