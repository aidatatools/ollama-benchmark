import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()  # Return the output of the command
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}': {e}")
        return None

def check_ollama_version():
    res = run_command(['ollama', '--version'])
    #print(res)
    return res[18:]

if __name__ == "__main__":
    check_ollama_version()