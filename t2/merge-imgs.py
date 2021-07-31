import cv2


def main():
    im1 = cv2.imread('t2/images/address_mel_spectogram.png')
    im2 = cv2.imread('t2/images/address_mfcc.png')
    im_h = cv2.hconcat(im1, im2)

    cv2.imwrite('t2/images/address_concat.png', im_h)

    im1 = cv2.imread('t2/images/secs-mel-spectogram.png')
    im2 = cv2.imread('t2/images/secs-mfcc.png')
    im_h = cv2.hconcat(im1, im2)

    cv2.imwrite('t2/images/secs_concat.png', im_h)


if __name__ == '__main__':
    main()