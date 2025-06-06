# DETECCAO DE SINAIS EM VERDE
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

    if len(greenContours) > 0:
        greenDetected = True
        green_x, green_y, green_w, green_h = cv2.boundingRect(greenContours[0])        
        green_centerx = green_x + (green_w // 2)
        cv2.line(frame, (green_centerx, 200), (green_centerx, 250), (0, 0, 255), 3)

    if len(blackContours) > 0:
        black_x, black_y, black_w, black_h = cv2.boundingRect(blackContours[0])
        black_centerx = black_x + (black_w // 2)
        cv2.line(frame, (black_centerx, 200), (black_centerx, 250), (255, 0, 0), 3)
    
    # VIRAR A ESQUERDA
    if greenDetected and green_centerx < black_centerx:
        cv2.putText(frame, "Turn Left", (50, 180), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
    
    # VIRAR A DIREITA
    elif greenDetected and green_centerx > black_centerx:
        cv2.putText(frame, "Turn Right", (350, 180), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
    
    # SEGUIR A LINHA
    elif len(blackContours) > 0:
        setpoint = 320
        error = black_centerx - setpoint
        centerText = "Error = " + str(error)
        cv2.putText(frame, centerText, (200, 340), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)
    
    # NENHUM SINAL (POSSIVEL GAP)
    else:
        cv2.putText(frame, "Nenhum sinal detectado", (200, 340), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)
        
    cv2.imshow("Orientacao de movimento", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# FINALIZACAO
cv2.destroyAllWindows()
picam2.close()
