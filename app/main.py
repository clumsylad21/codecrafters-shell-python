import sys
import os
import subprocess

BUILTINS = ["echo", "exit", "type", "pwd"]


def find_executable(cmd):
    for directory in os.environ.get("PATH", "").split(os.pathsep):
        full_path = os.path.join(directory, cmd)

        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path

    return None


def run_command(cmd, args):
    if cmd == "echo":
        print(" ".join(args))

    elif cmd == "exit":
        sys.exit(0)

    elif cmd == "pwd":
        print(os.getcwd())

    elif cmd == "cd":
        target = args[0] if args else os.path.expanduser("~")

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
            subprocess.run([cmd] + args, executable=executable)
        else:
            print(f"{cmd}: command not found")


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        user_input = sys.stdin.readline().strip()
        parts = user_input.split()

        if not parts:
            continue

        cmd = parts[0]
        args = parts[1:]

        run_command(cmd, args)


if __name__ == "__main__":
    main()