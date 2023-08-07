import logging
import click
import deeplake
import numpy as np
from PIL import Image, ImageDraw
import deeplake

logging.basicConfig(level=logging.INFO)


@click.command()
@click.option("--deeplake_path", help="Path to the deeplake dataset")
@click.option("--saved_path", help="Saved path for deep lake and visualize result")
def visualize(deeplake_path: str, saved_path: str) -> None:
    """
    Visualize an image

    Parameters:
        deeplake_path (str): Path to the deeplake dataset
        saved_path (str): Saved path for visualize result
    """
    logging.info("Load Deep Lake dataset")
    ds = deeplake.load(deeplake_path)
    logging.info("Load successfully")

    # Draw bounding boxes for the fourth image
    ind = 1
    img = Image.fromarray(ds.images[ind].numpy())
    draw = ImageDraw.Draw(img)
    (w,h) = img.size
    boxes = ds.boxes[ind].numpy()

    for b in range(boxes.shape[0]):
        (xc,yc) = (int(boxes[b][0]*w), int(boxes[b][1]*h))
        (x1,y1) = (int(xc-boxes[b][2]*w/2), int(yc-boxes[b][3]*h/2))
        (x2,y2) = (int(xc+boxes[b][2]*w/2), int(yc+boxes[b][3]*h/2))
        draw.rectangle([x1,y1,x2,y2], width=2)
        draw.text((x1,y1), ds.labels.info.class_names[ds.labels[ind].numpy()[b]])

    img.save(saved_path + '/test_img.jpg')
    logging.info(f"Image saved at {saved_path + '/test_img.jpg'}")

if __name__ == "__main__":
    visualize()
