from darknet import print_detections
from darknet_images import *
import darknet

def save_bbox(name, image, detections, class_names):
    file_name = os.path.splitext(name)[0] + ".txt"
    with open(file_name, "w") as f:
        for label, confidence, bbox in detections:
            x, y, w, h = convert2relative(image, bbox)
            label = class_names.index(label)
            f.write("{} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f}\n".format(label, x, y, w, h, float(confidence)))


def main():
    args=parser()
    net, class_names, class_colors=darknet.load_network(args.config_file,args.data_file, 
                                                        args.weights, batch_size=args.batch_size)

    image_name='image4.jpg'
    image, detections=image_detection(image_name, net, class_names, class_colors, args.thresh)
    save_bbox(image_name, image, detections, class_names)
    print_detections(detections, args.ext_output)

if __name__=='__main__':
    main()    
