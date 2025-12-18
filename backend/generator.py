from typing import List, Dict, Any, Set
from collections import deque

def generate_pytorch_code(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> str:
    """
    Generates PyTorch code from a graph of nodes and edges.
    1. Organize nodes by ID.
    2. Build adjacency list.
    3. Topological sort to determine execution order.
    4. Generate __init__ (layer definitions).
    5. Generate forward (function calls).
    """
    
    node_map = {n['id']: n for n in nodes}
    adj = {n['id']: [] for n in nodes}
    in_degree = {n['id']: 0 for n in nodes}
    
    # Build graph
    for edge in edges:
        src = edge['source']
        tgt = edge['target']
        if src in adj and tgt in in_degree:
            adj[src].append(tgt)
            in_degree[tgt] += 1
            
    # Topological sort
    queue = deque([n_id for n_id, d in in_degree.items() if d == 0])
    sorted_nodes = []
    
    while queue:
        u = queue.popleft()
        sorted_nodes.append(node_map[u])
        
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
                
    if len(sorted_nodes) != len(nodes):
        return "# Error: Graph contains a cycle or disconnected components."

    # Code Construction
    imports = "import torch\nimport torch.nn as nn\nimport torch.nn.functional as F\n\n"
    class_def = "class GeneratedModel(nn.Module):\n    def __init__(self):\n        super(GeneratedModel, self).__init__()\n"
    
    init_lines = []
    forward_lines = ["    def forward(self, x):\n"]
    
    # Track variable names for forward pass
    # Output of node_id is stored in var_map[node_id]
    var_map = {} 
    
    # Defaults for layers (since UI doesn't edit them yet)
    # Note: These defaults are fallbacks. The actual params come from frontend user input now.
    # However, we keep this list to validate "known" types.
    known_types = {
        'nn.Linear', 
        'nn.Conv2d', 'nn.MaxPool2d', 'nn.AvgPool2d', 
        'nn.ReLU', 'nn.Sigmoid', 'nn.Tanh', 'nn.Softmax',
        'nn.BatchNorm2d', 'nn.LayerNorm', 'nn.Dropout',
        'nn.Flatten',
        'nn.Embedding',
        'nn.Transformer', 
        'nn.TransformerEncoderLayer', 
        'nn.TransformerDecoderLayer'
    }
    
    for i, node in enumerate(sorted_nodes):
        n_id = node['id']
        n_data = node.get('data', {})
        n_type = n_data.get('layerType', 'input')
        n_params = n_data.get('params', {})
        
        # Safe variable name
        safe_id = n_id.replace('-', '_')
        layer_name = f"layer_{safe_id}"
        
        if n_type == 'input' or 'Input' in n_data.get('label', ''):
            var_map[n_id] = "x"
            continue
            
        # Define layer in __init__
        if n_type in known_types:
            # Construct param string, e.g., "in_channels=3, out_channels=16"
            param_str_list = []
            for k, v in n_params.items():
                param_str_list.append(f"{k}={v}")
            
            param_str = ", ".join(param_str_list)
            
            init_lines.append(f"        self.{layer_name} = {n_type}({param_str})")
        else:
             init_lines.append(f"        # Unknown layer type: {n_type}")
        
        # Define call in forward
        incoming_sources = [e['source'] for e in edges if e['target'] == n_id]
        
        if not incoming_sources:
             input_var = "x" 
        else:
            # If multiple inputs, we only take first for now. 
            # TODO: Handle Concat/Add layers for multiple inputs
            input_var = var_map.get(incoming_sources[0], "x")
            
        var_map[n_id] = f"out_{safe_id}"
        
        # Handle Flatten specially if needed, but nn.Flatten is a module, so it works same way
        forward_lines.append(f"        {var_map[n_id]} = self.{layer_name}({input_var})")

    # Combine
    if not init_lines:
        init_lines.append("        pass")
        
    full_code = imports + class_def + "\n".join(init_lines) + "\n\n" + "\n".join(forward_lines) + f"        return {var_map.get(sorted_nodes[-1]['id'], 'x')}\n"
    
    return full_code
