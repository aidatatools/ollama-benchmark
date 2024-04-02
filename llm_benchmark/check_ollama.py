import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()  # Return the output of the command
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}': {e}")
        return None

def check_ollama_version(ollamabin='ollama'):
    res = run_command([ollamabin, '--version'])
    ans = res.split('\n')
    #print(ans[-1])
    if("warning" in ans[-1].lower()):
        return ans[-1][27:]
    else:
        return ans[-1][18:]

if __name__ == "__main__":
    check_ollama_version()
    check_ollama_version('ollama')