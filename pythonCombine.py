from cgi import escape
from urllib import unquote
from mod_python import apache, util
import json
import numpy as np, cv2


def hex_to_bgr(value):
value = value.lstrip('#')
lv = len(value)
r, g, b = tuple(int(value[i: i + lv / 3], 16) for i in range(0, lv, lv / 3))
return [b, g, r, 255]


# The Publisher passes the Request object to the function
def index(req,jsonText):
#GET parameter!!!
# parameters = util.FieldStorage(req)
# jsonParam = parameters.get("json", "d")
#req.write(json)

jsons = json.loads(jsonText)
img = np.zeros((600, 600, 4), np.uint8)
#img = cv2.CreateImage((600,600),8,3)
#cv2.rectangle(img,(0,0),(600,600),(155,155,155,255),thickness=-1)

croptop = int(jsons["top"])
cropleft = int(jsons["left"])
cropheight = int(jsons["height"])
cropwidth = int(jsons["width"])
resultwidth = int(jsons["fw"])
resultheight = int(jsons["fh"])
cropradius = int(jsons["radius"])
bghexcode = jsons["background"]

bgcolor = hex_to_bgr(bghexcode)
#bgcolor = np.uint8([[bgcolor]]))
#bgcolor = cv2.cvtColor(bgcolor, cv2.COLOR_BGRA2RGBA)
cv2.circle(img,((cropleft+cropwidth/2),(croptop+cropheight/2)),cropradius,bgcolor,thickness=-1)
# cv2.circle(img,(305,230),cropradius,(234,206,149,255),thickness=-1)

for layer in jsons["layerList"]:
transform = layer["transform"].split(",")
tmp = cv2.imread("/mnt/nas/aItemImages/" + layer["imagePath"],-1)

y_offset = int(transform[5])
x_offset = int(transform[4])
for c in range(0,3):
img[y_offset:y_offset + tmp.shape[0], x_offset:x_offset + tmp.shape[1], c] = tmp[:,:,c] * (tmp[:,:,3]/255.0) + img[y_offset:y_offset + tmp.shape[0], x_offset:x_offset + tmp.shape[1], c] * (1.0 - tmp[:,:,3]/255.0)

croptopend = (cropheight+croptop)
cropleftend = (cropwidth+cropleft)
img = img[croptop:croptopend,cropleft:cropleftend,:]
img = cv2.resize(img, (resultwidth,resultheight))

#height,width,depth = img.shape
#circle_img = np.zeros((height,width), np.uint8)
#cv2.circle(circle_img,(width/2,height/2),75,(255,255,255),thickness=-1)
#masked_data = cv2.bitwise_and(img, img, mask=circle_img)

#img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
cv2.imwrite("/home1/irteam/deploy/switch-api/py/yresult.png",img,[cv2.IMWRITE_PNG_COMPRESSION,9])

#req.write(stringData)
req.sendfile("/home1/irteam/deploy/switch-api/py/yresult.png");
return apache.OK
