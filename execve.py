import subprocess
import tempfile
import os


def execute_code(language, code):
    suffix = get_file_extension(language)
    fd, filepath = tempfile.mkstemp(suffix=suffix, dir='/tmp/')
    with os.fdopen(fd, 'w') as tmp:
        tmp.write(code)

    if language == 'py':
        command = f"python {filepath}"
    elif language == 'cpp':
        compile_command = f"g++ {filepath} -o {filepath}.exe"
        run_command = f"{filepath}.exe"
        subprocess.run(compile_command, shell=True)
        command = run_command
    else:
        raise ValueError("Unsupported language")

    try:
        process = subprocess.run(
            command, shell=True, capture_output=True, timeout=5)
        stdout = process.stdout.decode('utf-8').strip()
        stderr = process.stderr.decode('utf-8').strip()

        # Nettoyage
        if language == 'cpp':
            os.remove(f"{filepath}.exe")
        os.remove(filepath)

        return stdout, stderr
    except subprocess.TimeoutExpired:
        # Nettoyage en cas de dépassement du délai
        if language == 'cpp':
            os.remove(f"{filepath}.exe")
        os.remove(filepath)
        return "Execution timed out.", ""


def get_file_extension(language):
    if language == 'py':
        return '.py'
    elif language == 'cpp':
        return '.cpp'
    else:
        raise ValueError("Unsupported language")
