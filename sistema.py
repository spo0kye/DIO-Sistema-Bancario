import msvcrt

def main() -> None:
    char = str(msvcrt.getche())
    print(f"Hello, {char}!")
    
if __name__ == "__main__":
    main()