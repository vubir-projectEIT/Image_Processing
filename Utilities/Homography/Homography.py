import cv2
import numpy as np


def _preprocess(image, lower=np.array([0, 0, 100]), upper=np.array([179, 90, 255])):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask_image = cv2.inRange(hsv_image, lower, upper)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 30))
    dilated_image = cv2.dilate(mask_image, kernel, iterations=1)
    preprocessed_image = 255 - cv2.bitwise_and(dilated_image, mask_image)
    return preprocessed_image

def create_flat_board(tile_size=100, pattern_size=(7,7)):
    flat_chessboard = [[[tile_size*(x+1), tile_size*(y+1)]] for y in range(pattern_size[1]) for x in range(pattern_size[0])]
    flat_chessboard_array = np.array(flat_chessboard).reshape(-1, 1, 2)
    flat_chessboard = np.zeros((pattern_size[0]+1, pattern_size[1]+1))
    return flat_chessboard, flat_chessboard_array

def homography_transform(image, tile_size=20, pattern_size=(7,7), flat_chessboard_array=None):
    preprocessed_image = _preprocess(image)
    ret, corners = cv2.findChessboardCorners(preprocessed_image, pattern_size)

    if ret:
        if flat_chessboard_array is None:
            _, flat_chessboard_array = create_flat_board(tile_size, pattern_size)
        H, _ = cv2.findHomography(corners, flat_chessboard_array)
        transformed_image = cv2.warpPerspective(image, H, ((pattern_size[0] + 1) * tile_size + 1, (pattern_size[1] + 1) * tile_size + 1))

        for i in range(pattern_size[0]+2):
            cv2.line(transformed_image, (tile_size*i,0), (tile_size*i,(pattern_size[1]+2)*tile_size), (0,0,255), 1)
        for i in range(pattern_size[1]+2):
            cv2.line(transformed_image, (0,tile_size*i), ((pattern_size[0]+2)*tile_size,tile_size*i), (0,0,255), 1)
        return transformed_image

    else:
        return None

if __name__ == "__main__":

    tile_size = 50
    pattern_size = (7, 7)

    flat_chessboard, flat_chessboard_array = create_flat_board(tile_size, pattern_size)

    image = cv2.imread("kFM1C.jpg")
    transformed_image = homography_transform(image, tile_size, pattern_size, flat_chessboard_array)

    cv2.imshow("raw", image)
    cv2.imshow("homography", transformed_image)
    cv2.waitKey(0)