# motecpy

Python library to decode CAN data from a MoTeC M84 ECU. The MoTeC outputs a unique CAN message set where the arbitration ID is unchanging. There is only a start and end frame, and the data inbetween. This may not have all the data-points covered, but it should help get you started. There is also an included PDF with the data set from MoTeC if you want more information.

To install just dump 'motecpy.py' in your project directory and include it in your program. motecpy works with socketcan, however I'm sure you can adjust it to work with whatever you need (it's only 200 lines of code, not that complex). I wouldn't trust 'setup.py', I made that over 3 years ago. No clue on if it works or not. I've since moved onto better ECUs. 

If you have any questions, feel free to message/email me at [ajstamps@gmail.com](mailto:ajstamps@gmail.com).
