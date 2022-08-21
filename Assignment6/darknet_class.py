import cv2
import darknet
import time


class Detection:

    def __init__(self, config_file, data_file, weight_file, darknet_width, darknet_height):

        self.network, self.class_names, self.class_colors = darknet.load_network(config_file, data_file, weight_file)
        self.darknet_width = darknet_width
        self.darknet_height = darknet_height

    def convert2relative(self, bbox, darknet_height, darknet_width):
        x, y, w, h = bbox
        _height = darknet_height
        _width = darknet_width
        return x / _width, y / _height, w / _width, h / _height

    def convert2original(self, image, bbox, darknet_height, darknet_width):
        x, y, w, h = model.convert2relative(bbox, darknet_height, darknet_width)

        image_h, image_w, __ = image.shape

        orig_x = int(x * image_w)
        orig_y = int(y * image_h)
        orig_width = int(w * image_w)
        orig_height = int(h * image_h)

        bbox_converted = (orig_x, orig_y, orig_width, orig_height)

        return bbox_converted

    def detect(self, frame):

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (self.darknet_width, self.darknet_height),
                                   interpolation=cv2.INTER_LINEAR)
        img_for_detect = darknet.make_image(self.darknet_width, self.darknet_height, 3)
        darknet.copy_image_from_bytes(img_for_detect, frame_resized.tobytes())
        detections = darknet.detect_image(self.network, self.class_names, img_for_detect, thresh=0.25)
        darknet.print_detections(detections)
        return detections

    def draw(self, frame, results):
        detections_adjusted = []
        img = frame
        detections = results
        if frame is not None:
            for label, confidence, bbox in detections:
                bbox_adjusted = model.convert2original(frame, bbox, self.darknet_height, self.darknet_width)
                detections_adjusted.append((str(label), confidence, bbox_adjusted))
            image = darknet.draw_boxes(detections_adjusted, frame, self.class_colors)
            return image


if __name__ == '__main__':

    input_path = 'videoplayback.mp4'
    config_file = '/home/ahmet/darknet/cfg/yolov4-custom.cfg'
    data_file = '/home/ahmet/Desktop/yolov4-custom-tiny (copy)/darknet/data/coco.data'
    weight_file = '/home/ahmet/darknet/yolov4.weights'

    cap = cv2.VideoCapture(input_path)

    darknet_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    darknet_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    model = Detection(config_file, data_file, weight_file, darknet_width, darknet_height)
    while cap.isOpened():

        t1 = time.time()
        ret, frame = cap.read()
        t2 = time.time()
        if ret:
            results = model.detect(frame)  # class and their bbox
            print(results)
            sonuc = model.draw(frame, results)

            cv2.imshow('detections', sonuc)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


