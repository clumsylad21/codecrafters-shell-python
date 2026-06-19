import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    while True:
     sys.stdout.write("$ ")
    
     command = input()
     if command == "exit":
         break
     elif command.startswith("echo"):
            print(command[5:])
     else:
         print(f"{command}: command not found")


if __name__ == "__main__":
    main()
