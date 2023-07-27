import numpy as np

def read_yolo_boxes(fn:str):
    """
    Function reads a label.txt YOLO file and returns a numpy array of yolo_boxes 
    for the box geometry and yolo_labels for the corresponding box labels.
    """
    
    with open(fn) as box_f:
        lines = box_f.read()
    
    # Split each box into a separate lines
    lines_split = lines.splitlines()
    
    yolo_boxes = np.zeros((len(lines_split),4))
    yolo_labels = np.zeros(len(lines_split))
    
    # Go through each line and parse data
    for l, line in enumerate(lines_split):
        line_split = line.split()
        yolo_boxes[l,:]=np.array((float(line_split[1]), float(line_split[2]), float(line_split[3]), float(line_split[4])))
        yolo_labels[l]=int(line_split[0]) 
         
    return yolo_boxes, yolo_labels