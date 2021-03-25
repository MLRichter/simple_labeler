This is a very simple, very straight forward GUI for labeling binary classified images.
"Y" and "N"-Buttons reference the positive (Symbol) and negative (No Symbol) label. Pressing the Enter-Button quits the 
application without making changes to the filesystem.
The code is mostly me teaching myself a little bit of building GUIs in Python. So no gurantee for the quality.

# Usage 

````

python main.py -i E:\inaturalist\train\Birds202 -o .\banana_apple_monkey.csv

````

The "-i" is representing the input folder, "-o" the output file.
The output file will also be used as a checkpoint.
The system will automatically skip all things labeled "keep" when loaded from 
a checkpoint.
The system is not able to search recursivly through a folder, it will only look
into the top level folder you specified.
