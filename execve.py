import subprocess
import tempfile
import os


def get_file_extension(language):
    if language == 'py':
        return '.py'
    elif language == 'cpp':
        return '.cpp'
    elif language == 'c':
        return '.c'
    elif language == 'java':
        return '.java'
    elif language == 'zig':
        return '.zig'
    else:
        raise ValueError("Unsupported language")


def compile_and_run(filepath, compiler):
    executable = filepath + ".exe"
    subprocess.run([compiler, filepath, "-o", executable],
                   capture_output=True, timeout=5)
    return [executable]


def execute_code(language, code):
    lang_config = {
        'py':   {'ext': '.py',   'command': lambda path: ["python", path]},
        'cpp':  {'ext': '.cpp',  'command': lambda path: compile_and_run(path, "g++")},
        'c':    {'ext': '.c',    'command': lambda path: compile_and_run(path, "gcc")},
        'java': {'ext': '.java', 'command': lambda path: ["java", path]},
        'zig':  {'ext': '.zig',  'command': lambda path: ["zig", "run", path]}
    }

    if language not in lang_config:
        raise ValueError("Unsupported language")

    suffix = lang_config[language]['ext']
    command_func = lang_config[language]['command']

    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False, mode='w', encoding='utf-8') as tmp:
            tmp.write(code)
            filepath = tmp.name

        command = command_func(filepath)
        process = subprocess.run(command, capture_output=True, timeout=5)
        stdout = process.stdout.decode('utf-8').strip()
        stderr = process.stderr.decode('utf-8').strip()

        return stdout, stderr

    except subprocess.TimeoutExpired:
        return "Execution timed out.", ""
    finally:
        if language in ['cpp', 'c']:
            os.remove(filepath + ".exe")
        if os.path.exists(filepath):
            os.remove(filepath)
