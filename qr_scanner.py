import cv2, time, qr_code_generator
from pyzbar.pyzbar import decode
import numpy as np

cam = cv2.VideoCapture(0) # Camera
width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH)) # Camera width
height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT)) # Camera height
distance = 140*(height/480)
point = [(int(width/2 - distance), int(height/2 - distance)),(int(width/2 + distance), int(height/2 + distance))]
scan = cv2.imread("scan.png") # Scan icon
scan1 = cv2.imread("scan.png") # Scan icon
scan = cv2.resize(scan, (width, height)) # Resize them according to width and height
scan1 = cv2.resize(scan1, (width, height))
not_read = [255,177,9] # blue when not read
read = [63,209,38] # green when read
scan1[np.where((scan == not_read).all(axis = 2))] = read # scan1 is green

def unlock_wait(gate):
    while(gate == True):
        if cv2.waitKey(1) == ord('q'): # If you press 'q' button, camera will be activated.
            gate = False
    return gate

def camera_open():
    unlocked = False
    while cam.isOpened():
        _, frame = cam.read()
        frame1 = cv2.add(scan, frame)
        
        cv2.imshow("QR Code Scanner", frame1) # show the frame
        key = cv2.waitKey(1)

        for i in decode(frame): # decode the frame
            rect = i.rect # i is qrcode object
            if (rect.left >= point[0][0] and rect.top >= point[0][1] and (rect.left + rect.width) <= point[1][0] and (rect.top + rect.height) <= point[1][1]): # if  i is in scan area
                print(i.data.decode('utf-8')) # print the data
                initialcodecontrol = (i.data.decode('utf-8')[:len(qr_code_generator.initial_code)] == qr_code_generator.initial_code) # control initial part
                codelengthcontrol = (len(i.data.decode('utf-8')) == qr_code_generator.codelength) # and control length
                if(initialcodecontrol and codelengthcontrol): # if both are true
                    if(unlocked == False):
                        unlocked = True # unlocks the gate and locks the camera
                        frame1 = cv2.add(scan1, frame)
                        frame1 = cv2.putText(frame1, 'Kilit açıldı.', (50,50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2, cv2.LINE_AA) # Inform user gate is unlocked.
                        cv2.imshow("QR Code Scanner", frame1)
                        cv2.waitKey(1)
                        time.sleep(1)
                        unlocked = unlock_wait(unlocked)
                else: #else
                    frame1 = cv2.putText(frame1, 'Geçersiz QR kod.', (50,50), cv2.FONT_HERSHEY_SIMPLEX,  
                    1, (0, 0, 255), 2, cv2.LINE_AA) # Inform user qrcode is invalid.
                    cv2.imshow("QR Code Scanner", frame1)
                    cv2.waitKey(1)
        if key == 27:
            break
if __name__ == '__main__':
    camera_open()

cam.release()
cv2.destroyAllWindows()
