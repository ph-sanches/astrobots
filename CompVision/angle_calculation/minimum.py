# TESTE DE DETECCAO DE AREA DE LINHA MINIMA
# ROBOTICA - CEFET/RJ UNED PETROPOLIS
# ALTERADO PELA ULTIMA VEZ EM: 28/O5/2025

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
    
    frame = picam2.capture_array()
    kernel = np.ones((3, 3), np.uint8)
    
    black_line = cv2.inRange(frame, (0, 0, 0), (50, 50, 50))
    black_line = cv2.erode(black_line, kernel, iterations = 5)
    black_line = cv2. dilate(black_line, kernel, iterations = 9)
   
    black_contours, black_hierarchy = cv2.findContours(black_line.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(black_contours) > 0:
        
        x_bound, y_bound, w_bound, h_bound = cv2.boundingRect(black_contours[0])
        cv2.rectangle(frame, (x_bound, y_bound), (x_bound + w_bound, y_bound + + h_bound), (255, 0, 0), 3)
        
        black_box = cv2.minAreaRect(black_contours[0])
        (x_min, y_min), (w_min, h_min), ang = black_box
        ang = int(ang)
        box = cv2.boxPoints(black_box)
        box = np.int0(box)
        cv2.drawContours(frame, [box], 0, (0, 0, 255), 3)
        cv2.putText(frame, str(ang), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Retângulo mínimo e área mínima", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# FINALIZACAO
cv2.destroyAllWindows()
picam2.close()