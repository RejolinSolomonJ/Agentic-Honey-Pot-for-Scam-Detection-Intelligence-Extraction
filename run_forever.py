import subprocess
import time
import sys
import threading

def run_uvicorn():
    try:
        # Start the server on port 8080
        with open("server_log.txt", "w") as out:
            subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8080"], stdout=out, stderr=out)
    except Exception as e:
        with open("server_error.txt", "w") as f:
            f.write(str(e))

def run_ssh_tunnel():
    try:
        # Start SSH tunnel and capture output to find the URL
        process = subprocess.Popen(
            ["ssh", "-o", "StrictHostKeyChecking=no", "-R", "80:127.0.0.1:8080", "serveo.net"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        with open("connection_info.txt", "w") as f:
            f.write("Starting...\n")
            
        # Monitor output for the URL
        for line in process.stdout:
            if "serveo.net" in line or "http" in line:
                with open("connection_info.txt", "a") as f:
                    f.write(line)
                    f.flush()
    except Exception as e:
        with open("tunnel_error.txt", "w") as f:
            f.write(str(e))
                
if __name__ == "__main__":
    # Start server in thread
    t1 = threading.Thread(target=run_uvicorn)
    t1.daemon = True
    t1.start()
    
    time.sleep(3)
    
    # Start tunnel
    run_ssh_tunnel()
