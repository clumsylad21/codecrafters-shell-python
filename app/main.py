import sys
import os

BUILTINS = ["echo", "exit", "type"]

def run_command(cmd, arg):
    if cmd == "echo":
        print(" ".join(arg))
    elif cmd == "exit":
        sys.exit(0)
    elif cmd == "type":
        target = arg[0] if arg else None
        if target in BUILTINS:
            print(f"{target} is a shell builtin")
            return
        else:
            for directory in os.environ.get("PATH", "").split(os.pathsep):
                full_path = os.path.join(directory, target)
                if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                    print(f"{target} is {full_path}")
                    return
                
        print(f"{target} not found")
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
