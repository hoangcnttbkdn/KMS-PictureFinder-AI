import openpifpaf

class UpperCrop:
    def __init__(self, checkpoint="shufflenetv2k16"):
        # Load model
        self.predictor = openpifpaf.Predictor(checkpoint=checkpoint)

    def __call__(self, opencv_image):
        keypoints = self.run_inference(opencv_image)
        images = self.crop_image(keypoints, opencv_image)
        return images

    def run_inference(self, opencv_image):
        predictions, gt_anns, meta = self.predictor.numpy_image(opencv_image)
        return predictions

    def crop_image(self, output, image):
        images = []
        for keypoint in output:
            # plot_skeleton_kpts(nimg, output[idx, 7:].T, 3)
            if keypoint.score < 0.5:
                continue
            keypoint = keypoint.data

            xs, ys = [], []
            for i in [6, 12, 5, 11]:
                x, y, conf = keypoint[i]
                xs.append(int(x))
                ys.append(int(y))

            x1, y1, x2, y2 = min(xs), min(ys), max(xs), max(ys)
            if (x1 >= x2
                or y1 >= y2
                or x1 < 0
                or y1 < 0
                    or max(y2-y1, x2-x1)/min(y2-y1, x2-x1) > 3):
                continue
            images.append(image[y1:y2, x1:x2])
        return images
