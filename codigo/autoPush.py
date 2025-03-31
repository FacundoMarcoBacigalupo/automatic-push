import os
from datetime import datetime
import subprocess

commit_message = "Update"
project_path = r"ubicacion del project"

def modify_file():
    file_path = os.path.join(project_path, "test.txt")
    try:
        with open(file_path, "a") as f:
            f.write(f"\n# Actualización automatica: {datetime.now()}")
        print(f"Archivo modificado exitosamente: {file_path}")
    except Exception as e:
        print(f"Error al modificar el archivo: {e}")

def git_commands():
    os.chdir(project_path)
    try:
        # Verificar si estamos en medio de un rebase
        print("Verificando si hay un rebase en curso...")
        rebase_merge_path = os.path.join(project_path, ".git", "rebase-merge")
        if os.path.exists(rebase_merge_path):
            print("Rebase detectado. Abortando rebase...")
            subprocess.run(["git", "rebase", "--abort"], check=True, capture_output=True, text=True)

        # Confirmar cambios locales
        print("Confirmando cambios locales...")
        subprocess.run(["git", "add", "."], check=True, capture_output=True, text=True)

        # Verificar si hay cambios para confirmar
        print("Verificando si hay cambios para commit...")
        status_result = subprocess.run(["git", "status", "--porcelain"], check=True, capture_output=True, text=True)
        if not status_result.stdout.strip():
            print("No hay cambios nuevos para confirmar.")
        else:
            subprocess.run(["git", "commit", "-m", "Commit automático"], check=True, capture_output=True, text=True)
            print("Cambios confirmados con éxito.")

        # Comprobar si estamos en la rama correcta
        print("Comprobando la rama actual...")
        branch_result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], check=True, capture_output=True, text=True)
        current_branch = branch_result.stdout.strip()
        print(f"Rama actual: {current_branch}")

        if current_branch != "main":
            print("No estás en la rama 'main'. Cambiando de rama...")
            subprocess.run(["git", "checkout", "main"], check=True, capture_output=True, text=True)

        # git pull
        print("Ejecutando git pull...")
        pull_result = subprocess.run(["git", "pull", "--rebase"], check=True, capture_output=True, text=True)
        print("Resultado de git pull:")
        print(pull_result.stdout)

        # git push
        print("Ejecutando git push...")
        push_result = subprocess.run(["git", "push"], check=True, capture_output=True, text=True)

    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando comandos de Git: {e.stderr}")
    except Exception as e:
        print(f"Error desconocido: {e}")


if __name__ == "__main__":
    print("Modificando archivo...")
    modify_file()
    print("Ejecutando comandos de Git...")
    git_commands()