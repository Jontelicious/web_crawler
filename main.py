import sys

def main():

    print("Script name:", sys.argv[0])
    print("Argument:", sys.argv[1])

    if len(sys.argv) < 2:
        print("no website provided")
        return sys.exit(1)
    
    if len(sys.argv) > 2:
        print("too many arguments provided")
        return sys.exit(1)
    
    if len(sys.argv[1]) == 2:
        print(f"starting crawl of: {sys.argv[1]}")

if __name__ == "__main__":
    main()
