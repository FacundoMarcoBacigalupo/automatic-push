import win32serviceutil
import win32event
import time
import subprocess
import os

class GitAutoPushService(win32serviceutil.ServiceFramework):
    _svc_name_ = "GitAutoPushServicee"
    _svc_display_name_ = "GitAutoPushServicee"
    _svc_description_ = "Automatiza commits y pushes a GitHub una vez al día al iniciar el servicio."

    def __init__(self, args):
        super().__init__(args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.running = True
        self.log_file = r"ubicacion del service_log.txt"
        self.last_execution_date = None  # Guarda la fecha de la última ejecución

    def SvcStop(self):
        # Método llamado cuando el servicio se detiene.
        self.running = False
        win32event.SetEvent(self.stop_event)
        self.log_message("Servicio detenido.")

    def SvcDoRun(self):
        # Método principal que ejecuta el script una vez al día al iniciar el servicio.
        self.log_message("Servicio iniciado.")
        try:
            self.check_and_run_script()  # Ejecuta el script inmediatamente al iniciar
            while self.running:
                # Espera hasta 24 horas (86400 segundos) o hasta que se detenga el servicio
                result = win32event.WaitForSingleObject(self.stop_event, 86400 * 1000)  # 86400 segundos en milisegundos
                if result == win32event.WAIT_OBJECT_0:
                    break  # El servicio fue detenido
        except Exception as e:
            self.log_message(f"Error en el servicio: {e}")

    def check_and_run_script(self):
        current_date = time.strftime("%Y-%m-%d", time.localtime())  # Fecha actual (año-mes-día)
        if self.last_execution_date != current_date:  # Verifica si ya se ejecutó hoy
            self.run_script()
            self.last_execution_date = current_date  # Actualiza la última fecha de ejecución
        else:
            self.log_message("El script ya se ejecutó hoy. No se ejecutará de nuevo.")

    def run_script(self):
        # Ejecuta el script autoPush.py
        script_path = r"ubicacion del autoPush.py"
        if not os.path.exists(script_path):
            self.log_message(f"Script no encontrado: {script_path}")
            return

        try:
            self.log_message("Ejecutando script autoPush.py...")
            result = subprocess.run(["python", script_path], capture_output=True, text=True)
            self.log_message(f"Script ejecutado con éxito:\n{result.stdout}")
            if result.stderr:
                self.log_message(f"Errores encontrados al ejecutar el script:\n{result.stderr}")
        except Exception as e:
            self.log_message(f"Error al ejecutar el script: {e}")

    def log_message(self, message):
        # Escribe mensajes en un archivo de log.
        try:
            with open(self.log_file, "a") as log_file:
                log_file.write(f"{time.ctime()} - {message}\n")
        except Exception as e:
            print(f"Error escribiendo en el log: {e}")

if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(GitAutoPushService)