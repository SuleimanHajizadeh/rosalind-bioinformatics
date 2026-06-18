#!/usr/bin/env python3
import os

def tokenize(s):
    s = s.replace(" ", "").replace("\n", "").replace("\r", "")
    tokens = []
    i = 0
    n = len(s)
    while i < n:
        if s[i] in "(),;":
            tokens.append(s[i])
            i += 1
        else:
            j = i
            while j < n and s[j].isalpha():
                j += 1
            if j > i:
                tokens.append(s[i:j])
                i = j
            else:
                i += 1
    return tokens

def mate(x, y):
    x_AA, x_Aa, x_aa = x
    y_AA, y_Aa, y_aa = y
    
    z_AA = x_AA * y_AA + 0.5 * (x_AA * y_Aa + x_Aa * y_AA) + 0.25 * x_Aa * y_Aa
    z_aa = x_aa * y_aa + 0.5 * (x_aa * y_Aa + x_Aa * y_aa) + 0.25 * x_Aa * y_Aa
    z_Aa = x_AA * y_aa + x_aa * y_AA + 0.5 * (x_AA * y_Aa + x_Aa * y_AA + x_Aa * y_aa + x_aa * y_Aa) + 0.5 * x_Aa * y_Aa
    
    # Normalize to fix any floating point precision errors
    total = z_AA + z_Aa + z_aa
    if total > 0:
        z_AA /= total
        z_Aa /= total
        z_aa /= total
        
    return (z_AA, z_Aa, z_aa)

def parse(tokens, index):
    if index >= len(tokens):
        raise ValueError("Unexpected end of input")
        
    token = tokens[index]
    if token == '(':
        # Parse left child
        left, next_index = parse(tokens, index + 1)
        if next_index >= len(tokens) or tokens[next_index] != ',':
            raise ValueError(f"Expected ',' at token index {next_index}")
        # Parse right child
        right, next_index = parse(tokens, next_index + 1)
        if next_index >= len(tokens) or tokens[next_index] != ')':
            raise ValueError(f"Expected ')' at token index {next_index}")
        
        prob = mate(left, right)
        return prob, next_index + 1
    elif token in ["AA", "Aa", "aa"]:
        if token == "AA":
            prob = (1.0, 0.0, 0.0)
        elif token == "Aa":
            prob = (0.0, 1.0, 0.0)
        else:
            prob = (0.0, 0.0, 1.0)
        return prob, index + 1
    else:
        raise ValueError(f"Unknown token: {token} at index {index}")

def solve(newick_str):
    tokens = tokenize(newick_str)
    if not tokens:
        return (0.0, 0.0, 0.0)
    # The Newick string should end with ';' - remove it from token stream or handle it
    if tokens[-1] == ';':
        tokens = tokens[:-1]
    
    prob, next_index = parse(tokens, 0)
    if next_index != len(tokens):
        raise ValueError(f"Extraneous tokens starting at index {next_index}")
    return prob

def main():
    input_path = "rosalind_mend.txt"
    output_path = "output.txt"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    with open(input_path, 'r') as f:
        content = f.read().strip()
        
    if not content:
        print("Error: Input file is empty.")
        return
        
    prob = solve(content)
    output_str = f"{round(prob[0], 3)} {round(prob[1], 3)} {round(prob[2], 3)}"
    print("Computed Probabilities:", output_str)
    
    with open(output_path, 'w') as f:
        f.write(output_str + "\n")
    print(f"Result written to {output_path}")

if __name__ == "__main__":
    main()
