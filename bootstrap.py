import subprocess as os
if __name__ == '__main__':
    ip = input("IP:")
    with open("backend.js", "r") as file:          
        output = file.readlines()
        output[0] = f'host = "ws://{ip}:8081/"\n'
        with open("backend.js", "w") as out: 
            out.writelines(output)
    os.Popen(f"python -m http.server --bind {ip}")
    os.Popen(f"python WebSocket.py {ip}")
