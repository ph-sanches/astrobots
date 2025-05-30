# TESTE DE DETECCAO DE SINAIS EM VERDE
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

# EXIBICAO DE SINAIS EM VERDE
while True:
    greenDetected = False
    frame = picam2.capture_array()
    interest = frame[200:250, 0:639]
    kernel = np.ones((3, 3), np.uint8)
    
    blackLine = cv2.inRange(interest, (0, 0, 0), (50, 50, 50))
    blackLine = cv2.erode(blackLine, kernel, iterations = 5)
    blackLine = cv2. dilate(blackLine, kernel, iterations = 9)
    
    greenSign = cv2.inRange(frame, (0, 65, 0), (100, 200, 100))
    greenSign = cv2.erode(greenSign, kernel, iterations = 5)
    greenSign = cv2.dilate(greenSign, kernel, iterations = 9)
    
    blackContours, blackHierarchy = cv2.findContours(blackLine.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    greenContours, greenHierarchy = cv2.findContours(greenSign.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.imshow("Sinais Verdes", greenSign)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# FINALIZACAO
cv2.destroyAllWindows()
picam2.close()