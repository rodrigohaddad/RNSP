import cv2


def main():
    im1 = cv2.imread('t2/images/consusion-mel.png')
    im2 = cv2.imread('t2/images/confusion-mfcc.png')
    im_h = cv2.hconcat(im1, im2)

    cv2.imwrite('t2/images/confusion-concat.png', im_h)


if __name__ == '__main__':
    main()