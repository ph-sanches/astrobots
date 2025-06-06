# TESTE DE RETANGULO DELIMITADOR
# ROBOTICA - CEFET/RJ UNED PETROPOLIS
# ALTERADO PELA ULTIMA VEZ EM: 27/O5/2025

# IMPORTACAO DE BIBLIOTECAS
from picamera2 import Picamera2
import numpy as np
import cv2
import time

# INICIALIZACAO DA CAMERA
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

time.sleep(1)

# EXIBICAO DO RETANGULO
while True:
    frame = picam2.capture_array()
    interest = image[200:250, 0:639]
    blackLine = cv2.inRange(frame, (0, 0, 0), (50, 50, 50))
    kernel = np.ones((3, 3), np.uint8)
    blackLine = cv2.erode(blackLine, kernel, iterations = 5)
    blackLine = cv2. dilate(blackLine, kernel, iterations = 9)
    contours, hierarchy = cv2.findContours(blackLine.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
    if len(contours) > 0:
        x, y, w, h = cv2.boundingRect(contours[0])
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 3)
    cv2.imshow("Retangulo", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# FINALIZACAO
cv2.destroyAllWindows()
picam2.close()
