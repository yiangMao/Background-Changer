import cv2
import numpy as np
from rembg import remove


#capture person from given pic

inputPic = 'babypic.png'
backPic = 'bg1.jpg'
outputPic = 'babypicput.png'

# inputPic = 'tangtang.jpg'
# backPic = 'bg2.png'
# outputPic = "tangtang_out.jpg"


input_path = inputPic
output_path = outputPic

with open(input_path, 'rb') as i:
    with open(output_path, 'wb') as o:
        input = i.read()
        output = remove(input)
        o.write(output)


#overlay person with background

def overlay_transparent(background, overlay, x, y):

    bw = background.shape[1]
    bh = background.shape[0]

#adjust people pic and background pic size
    if x >= bw or y >= bh:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if bw*bh <= h*w:
        scale = (bw*bh)/(h*w)
        h = int(h*scale*0.5)
        w = int(w*scale*0.5)
        dim = (w,h)
        overlay = cv2.resize(overlay, dim, interpolation = cv2.INTER_AREA)

#    print("this is bg width", bw,"bg h: ",bh,"\n ov H",h,"ov w", w,"\nnew ov H", h, "new ov w",w)

    if x + w > bw:
        w = bw - x
        overlay = overlay[:, :w]

    if y + h > bh:
        h = bh - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
            ],
            axis = 2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image

    return background

background_img = cv2.imread(backPic)
overlay_img = cv2.imread(output_path,cv2.IMREAD_UNCHANGED)
orginal_img = cv2.imread(input_path)

#present background image, input image, portrait part of input image and the final output image
cv2.imshow("BackGround",background_img)
cv2.waitKey(0)


cv2.imshow("orginal",orginal_img)
cv2.waitKey(0)


cv2.imshow("over",overlay_img)
cv2.waitKey(0)

bw = background_img.shape[1]
bh = background_img.shape[0]

result = overlay_transparent(background_img,overlay_img,int(bw/2),int(bh/2))
cv2.imwrite('overlayResult.jpg',result)
cv2.imshow("result",result)
cv2.waitKey(0)
