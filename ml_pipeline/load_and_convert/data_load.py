import logging
import click
import deeplake
import numpy as np
import os

from utils import read_yolo_boxes

logging.basicConfig(level=logging.INFO)


@click.command()
@click.option("--data_path", help="Path to the image and boxes folder")
@click.option("--saved_path", help="Saved path for deeplake")
def data_load(data_path: str, saved_path: str) -> None:
    """
    Load data and save to a path

    Parameters:
        data_path (str): Path to the image and boxes folder
        saved_path (str): Path for deeplake dataset
    """
    logging.info("Create init Deep Lake dataset")
    if os.path.exists(saved_path + '/animals_od_deeplake'):
        logging.info("Deep Lake dataset exist!")
        ds = deeplake.load(saved_path + '/animals_od_deeplake')
    else:
        ds = deeplake.empty(saved_path + '/animals_od_deeplake')
        logging.info("Create init Deep Lake dataset successfully")

    logging.info("Reading dataset")
    img_folder = data_path + '/images'
    lbl_folder = data_path + '/boxes'

    # List of all images
    fn_imgs = os.listdir(img_folder)

    # List of all class names
    with open(os.path.join(lbl_folder, 'classes.txt'), 'r') as f:
        class_names = f.read().splitlines()
    logging.info("Read successfully.")

    # Create the tensors and iterate through all the images in the dataset in order to populate the data in Deep Lake
    logging.info("Create the tensors for Deep Lake")
    with ds:
        ds.create_tensor('images', htype='image', sample_compression = 'jpeg')
        ds.create_tensor('labels', htype='class_label', class_names = class_names)
        ds.create_tensor('boxes', htype='bbox')

        # Define the format of the bounding boxes
        ds.boxes.info.update(coords = {'type': 'fractional', 'mode': 'LTWH'})

        for fn_img in fn_imgs:

            img_name = os.path.splitext(fn_img)[0]
            fn_box = img_name+'.txt'

            # Get the arrays for the bounding boxes and their classes
            yolo_boxes, yolo_labels = read_yolo_boxes(os.path.join(lbl_folder,fn_box))
            
            # Append data to tensors
            ds.append({'images': deeplake.read(os.path.join(img_folder, fn_img)),
                    'labels': yolo_labels.astype(np.uint32),
                    'boxes': yolo_boxes.astype(np.float32)
                    })
    logging.info("Create successfully.")


if __name__ == "__main__":
    data_load()
