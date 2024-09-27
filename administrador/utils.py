import uuid    
import qrcode
from io import BytesIO
import base64


def get_tocken():
    # Generar una cadena larga con uuid.uuid4()
    cadena_larga = str(uuid.uuid4())
    # Extraer la primera subsecuencia antes del primer signo '-'
    subsecuencia = cadena_larga.split('-')[0]
    print(subsecuencia)
    return subsecuencia


def generate_qr_code(url):
    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer)
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_str