# TESTE DE MASCARA BINARIA
# ROBOTICA - CEFET/RJ UNED PETROPOLIS
# ALTERADO PELA ULTIMA VEZ EM: 27/O5/2025

# IMPORTACAO DE BIBLIOTECAS
from picamera2 import Picamera2
import cv2
import time

# INICIALIZACAO DA CAMERA
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

time.sleep(1)

# EXIBICAO DE MASCARA
while True:
    frame = picam2.capture_array()
    blackLine = cv2.inRange(frame, (0, 0, 0), (50, 50, 50))
    cv2.imshow("Original", frame)
    cv2.imshow("Mascara", blackLine)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# FINALIZACAO
cv2.destroyAllWindows()
picam2.close()