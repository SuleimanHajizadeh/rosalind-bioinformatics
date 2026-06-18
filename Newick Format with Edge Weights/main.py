import os
import sys
from collections import deque

class Node:
    def __init__(self, name="", children=None, weight=0):
        self.name = name
        self.children = children if children is not None else []
        self.weight = weight

def parse_node(s, pos):
    if pos >= len(s):
        return None, pos
    
    if s[pos] == '(':
        pos += 1  # Skip '('
        children = []
        while pos < len(s):
            child, pos = parse_node(s, pos)
            children.append(child)
            if pos < len(s) and s[pos] == ',':
                pos += 1  # Skip ','
            elif pos < len(s) and s[pos] == ')':
                pos += 1  # Skip ')'
                break
        
        # Parse name if any
        name_chars = []
        while pos < len(s) and s[pos] not in '(),:;':
            name_chars.append(s[pos])
            pos += 1
        name = "".join(name_chars).strip()
        
        # Parse weight if any
        weight = 0
        if pos < len(s) and s[pos] == ':':
            pos += 1  # Skip ':'
            weight_chars = []
            while pos < len(s) and s[pos] not in '(),;':
                weight_chars.append(s[pos])
                pos += 1
            weight = float("".join(weight_chars).strip())
            if weight.is_integer():
                weight = int(weight)
                
        return Node(name=name, children=children, weight=weight), pos
    else:
        # Leaf node
        name_chars = []
        while pos < len(s) and s[pos] not in '(),:;':
            name_chars.append(s[pos])
            pos += 1
        name = "".join(name_chars).strip()
        
        weight = 0
        if pos < len(s) and s[pos] == ':':
            pos += 1  # Skip ':'
            weight_chars = []
            while pos < len(s) and s[pos] not in '(),;':
                weight_chars.append(s[pos])
                pos += 1
            weight = float("".join(weight_chars).strip())
            if weight.is_integer():
                weight = int(weight)
                
        return Node(name=name, children=[], weight=weight), pos

def build_graph(node, parent_id=None, parent_weight=0, graph=None, node_counter=0):
    if graph is None:
        graph = {}
    
    # Assign a unique ID to this node if it doesn't have a name
    node_id = node.name if node.name else f"internal_{node_counter}"
    node_counter += 1
    
    if node_id not in graph:
        graph[node_id] = {}
        
    if parent_id is not None:
        graph[node_id][parent_id] = parent_weight
        graph[parent_id][node_id] = parent_weight
        
    for child in node.children:
        graph, node_counter = build_graph(
            child, 
            parent_id=node_id, 
            parent_weight=child.weight, 
            graph=graph, 
            node_counter=node_counter
        )
        
    return graph, node_counter

def find_distance(graph, start, end):
    queue = deque([(start, 0)])
    visited = {start}
    
    while queue:
        curr, dist = queue.popleft()
        if curr == end:
            return dist
            
        for neighbor, weight in graph[curr].items():
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + weight))
                
    return None

def solve_nkew(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} not found.")
        return
        
    with open(input_path, 'r') as f:
        lines = [line.strip() for line in f]
        
    blocks = []
    i = 0
    while i < len(lines):
        while i < len(lines) and not lines[i]:
            i += 1
        if i >= len(lines):
            break
        
        tree_line = lines[i]
        i += 1
        
        while i < len(lines) and not lines[i]:
            i += 1
        if i >= len(lines):
            break
        
        nodes_line = lines[i]
        i += 1
        
        blocks.append((tree_line, nodes_line))
        
    distances = []
    for idx, (tree_str, nodes_str) in enumerate(blocks):
        # Parse tree
        root_node, _ = parse_node(tree_str, 0)
        
        # Build graph
        graph, _ = build_graph(root_node)
        
        # Query nodes
        parts = nodes_str.split()
        if len(parts) != 2:
            print(f"Warning: Block {idx} has invalid target nodes line: '{nodes_str}'")
            continue
        start_node, end_node = parts
        
        # Find distance
        dist = find_distance(graph, start_node, end_node)
        if dist is not None:
            distances.append(str(dist))
        else:
            print(f"Warning: No path found between {start_node} and {end_node} in block {idx}")
            distances.append("0")
            
    result_str = " ".join(distances)
    
    with open(output_path, 'w') as f:
        f.write(result_str + '\n')
        
    print(f"Computed distances for {len(distances)} trees.")
    print(f"Result written to {output_path}")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_nkew.txt")
    output_file = os.path.join(script_dir, "output.txt")
    solve_nkew(input_file, output_file)
