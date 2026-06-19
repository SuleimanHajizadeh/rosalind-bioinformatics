import sys
import io

def main():
    # Capture stdout because 'import this' prints automatically to stdout when imported.
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    import this
    
    zen = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    with open("output.txt", "w") as out:
        out.write(zen)
        
    print("Zen of Python captured and written to output.txt.")

if __name__ == '__main__':
    main()
