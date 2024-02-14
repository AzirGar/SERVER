import os
import paramiko
from flask import Flask, request, jsonify, send_file
from flask import render_template
app = Flask(__name__)

# Especifica la ruta en tu servidor Linux donde deseas guardar los archivos
UPLOAD_FOLDER = '/home/dydetec/Files/'

# Configuración de la conexión SFTP
SFTP_HOST = '10.10.0.2'
SFTP_PORT = 22704
SFTP_USERNAME = 'dydetec'
SFTP_PASSWORD = 'Z0p0rt3'

def upload_to_sftp(file_path):
    with paramiko.Transport((SFTP_HOST, SFTP_PORT)) as transport:
        transport.connect(username=SFTP_USERNAME, password=SFTP_PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(file_path, os.path.join(UPLOAD_FOLDER, os.path.basename(file_path)))
        sftp.close()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No se encontró el archivo', 400
    
    file = request.files['file']
    file_path = os.path.join(os.path.expanduser("~"), "Documents", "files", file.filename)
    file.save(file_path)
    upload_to_sftp(file_path)
    os.remove(file_path)
    
    return 'Archivo cargado con éxito', 200

@app.route('/archivos', methods=['GET'])
def listar_archivos():
    try:
        with paramiko.Transport((SFTP_HOST, SFTP_PORT)) as transport:
            transport.connect(username=SFTP_USERNAME, password=SFTP_PASSWORD)
            sftp = paramiko.SFTPClient.from_transport(transport)
            archivos = sftp.listdir(UPLOAD_FOLDER)
            sftp.close()
            return render_template('listfiles.html', archivos=archivos)
    except Exception as e:
        return f'Error al listar archivos: {str(e)}', 500


def download_from_sftp(file_name):
    with paramiko.Transport((SFTP_HOST, SFTP_PORT)) as transport:
        transport.connect(username=SFTP_USERNAME, password=SFTP_PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get(os.path.join(UPLOAD_FOLDER, file_name), os.path.join(UPLOAD_FOLDER, file_name))
        sftp.close()

@app.route('/previsualizar', methods=['POST'])
def previsualizar_archivo():
    file_name = request.form['nombre_archivo']
    # Encuentra la ruta completa del archivo
    download_from_sftp(file_name)
    # Retorna el archivo
    return send_file(os.path.join(UPLOAD_FOLDER, file_name), as_attachment=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
