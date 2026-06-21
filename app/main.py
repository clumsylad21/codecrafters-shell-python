import sys
import os
import subprocess
import shlex
import readline

BUILTINS = ["echo", "exit", "type", "pwd", "cd"]
COMPLETABLE_BUILTINS = ["echo", "exit"]

def complete_input(text, state):
    line = readline.get_line_buffer()

    if " " in line:
        # Argument position: filename completion
        prefix = line.rsplit(" ", 1)[-1]

        matches = [
            filename
            for filename in os.listdir(".")
            if filename.startswith(prefix)
            and os.path.isfile(filename)
        ]

    else:
        # First word: existing builtin/executable completion
        matches = complete_command(text)

    matches = sorted(set(matches))

    if state < len(matches):
        return matches[state] + " "

    return None

def complete_command(text):
    matches = set()

    #Built-in matches
    for command in COMPLETABLE_BUILTINS:
        if command.startswith(text):
            matches.add(command)

    #Executable matches
    for directory in os.environ.get("PATH", "").split(os.pathsep):
        try:
            filenames = os.listdir(directory)
        except FileNotFoundError:
            continue

        for filename in filenames:
                if filename.startswith(text) and os.access(os.path.join(directory, filename), os.X_OK):
                    matches.add(filename)

    matches = sorted(matches)
    
    return matches

readline.set_completer(complete_input)
readline.set_completer_delims(" \t\n")
readline.parse_and_bind("tab: complete")

def find_executable(cmd):
    for directory in os.environ.get("PATH", "").split(os.pathsep):
        full_path = os.path.join(directory, cmd)

        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path

    return None


def run_command(cmd, args, stdout=None, stderr=None):
    output = stdout if stdout else sys.stdout
    error_output = stderr if stderr else sys.stderr

    if cmd == "echo":
        print(" ".join(args), file=output)

    elif cmd == "exit":
        sys.exit(0)

    elif cmd == "pwd":
        print(os.getcwd())

    elif cmd == "cd":
        target = args[0] 

        if target == "~":
            target = os.environ.get("HOME", os.path.expanduser("~"))

        try:
            os.chdir(target)
        except FileNotFoundError:
            print(f"cd: {target}: No such file or directory")
        except NotADirectoryError:
            print(f"cd: {target}: Not a directory")
        except PermissionError:
            print(f"cd: {target}: Permission denied")

    elif cmd == "type":
        target = args[0] if args else None

        if target in BUILTINS:
            print(f"{target} is a shell builtin")
            return

        executable = find_executable(target)

        if executable:
            print(f"{target} is {executable}")
        else:
            print(f"{target}: not found")

    else:
        executable = find_executable(cmd)

        if executable:
            subprocess.run([cmd] + args,
                            executable=executable,
                            stdout=stdout,
                            stderr=stderr)
        else:
            print(f"{cmd}: command not found", file=error_output)


def main():
    while True:
        try:
            user_input = input("$ ").strip()
        except EOFError:
            break
        parts = shlex.split(user_input)

        if not parts:
            continue

        cmd = parts[0]
        args = parts[1:]

        redirect_path = None
        stdout_path = None
        stderr_path = None
        redirect_mode = "w"  # Default write mode
        for operator in [">", "1>", "2>", ">>", "1>>", "2>>"]:
            if operator in args:
                idx = args.index(operator)
                redirect_path = args[idx + 1]
                args = args[:idx]  # Remove the redirection part

                if operator in [">>", "1>>"]:
                    stdout_path = redirect_path
                    redirect_mode = "a"  # Append mode
                elif operator in ["2>>"]:
                    stderr_path = redirect_path
                    redirect_mode = "a"  # Append mode
                elif operator == "2>":
                    stderr_path = redirect_path
                else:
                    stdout_path = redirect_path
                
                break

        if stdout_path:
            with open(stdout_path, redirect_mode) as output_file:
                run_command(cmd, args, stdout=output_file)
        elif stderr_path:
            with open(stderr_path, redirect_mode) as error_file:
                run_command(cmd, args, stderr=error_file)
        else:
            run_command(cmd, args)


if __name__ == "__main__":
    main()