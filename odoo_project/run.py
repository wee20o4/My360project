import subprocess
import time
import webbrowser

def wait_for_odoo():
    while True:
        try:
            subprocess.run(["curl", "-f", "http://localhost:8069"], timeout=5)
            print("✅ Odoo is ready!")
            break
        except subprocess.CalledProcessError:
            print("⏳ Waiting for Odoo...")
            time.sleep(5)

if __name__ == "__main__":
    subprocess.run(["docker-compose", "up", "--build", "-d"])
    wait_for_odoo()
    webbrowser.open("http://localhost:8069")