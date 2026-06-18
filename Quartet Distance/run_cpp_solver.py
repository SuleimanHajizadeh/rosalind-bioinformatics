import subprocess
import os

def main():
    # Read the input dataset
    input_path = "rosalind_qrtd.txt"
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    if len(lines) < 3:
        print("Error: Input file must contain taxa list and two tree strings.")
        return

    taxa = lines[0].split()
    t1_str = lines[1]
    t2_str = lines[2]

    # Ensure trees end with semicolon
    if not t1_str.endswith(";"):
        t1_str += ";"
    if not t2_str.endswith(";"):
        t2_str += ";"

    # Write trees to temporary files
    t1_file = "t1_temp.txt"
    t2_file = "t2_temp.txt"
    with open(t1_file, "w") as f:
        f.write(t1_str + "\n")
    with open(t2_file, "w") as f:
        f.write(t2_str + "\n")

    print(f"Taxa count: {len(taxa)}")
    print(f"Tree 1 length: {len(t1_str)} chars")
    print(f"Tree 2 length: {len(t2_str)} chars")

    # Run C++ binary
    binary_path = "./quartet-distance-main/quart_bin"
    if not os.path.exists(binary_path):
        print(f"Error: C++ binary {binary_path} not found. Please compile it first.")
        return

    # Command: ./quart_bin fancy calcQuartDist t1_temp.txt t2_temp.txt
    cmd = [binary_path, "fancy", "calcQuartDist", t1_file, t2_file]
    print(f"Running command: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error running C++ binary:")
        print(result.stderr)
        return

    output = result.stdout.strip()
    print(f"C++ binary output (disagreeing resolved quartets): {output}")
    
    try:
        val = int(output)
        final_dq = 2 * val
        print(f"Final Quartet Distance (2 * output): {final_dq}")
        
        # Save to output.txt
        with open("output.txt", "w") as f:
            f.write(str(final_dq) + "\n")
        print("Saved final answer to output.txt")
    except ValueError:
        print("Could not parse output as integer.")

    # Clean up temporary files
    if os.path.exists(t1_file):
        os.remove(t1_file)
    if os.path.exists(t2_file):
        os.remove(t2_file)

if __name__ == "__main__":
    main()
