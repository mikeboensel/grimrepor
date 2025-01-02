'''
Author: Akira Yoshiyama, 2024-12-29

WHAT DOES THIS DO?

This script parses the python files in a github repo and finds all the libraries used and the library functions/classes/etc.
used for each respectivelibrary.
'''

import ast
import os
from collections import defaultdict

def preprocess_python_file(file_path):
    # Read the file content
    with open(file_path, 'rb') as f:
        content = f.read()
    
    # Replace 'async=' with 'async_=' in the content
    modified_content = content.replace(b'async=', b'async_=')
    
    return modified_content 

class ImportUsageVisitor(ast.NodeVisitor):
    def __init__(self):
        self.imports = {}  # Stores import mappings (alias -> full name)
        self.usage = defaultdict(set)  # Tracks usage of imported items
        self.alias_to_original = {}  # Maps aliases to original package names
        
    def visit_Import(self, node):
        for alias in node.names:
            original_name = alias.name.split('.')[0]  # Get base package name
            if alias.asname:
                self.imports[alias.asname] = alias.name
                self.alias_to_original[alias.asname] = original_name
            else:
                self.imports[alias.name] = alias.name
                self.alias_to_original[alias.name] = original_name
                
    def visit_ImportFrom(self, node):
        module = node.module
        original_name = module.split('.')[0] if module else ''  # Get base package name
        for alias in node.names:
            if alias.asname:
                self.imports[alias.asname] = f"{module}.{alias.name}"
                self.alias_to_original[alias.asname] = original_name
            else:
                self.imports[alias.name] = f"{module}.{alias.name}"
                self.alias_to_original[alias.name] = original_name
                
    def visit_Name(self, node):
        # Check if the name is from our imports
        if isinstance(node.ctx, ast.Load) and node.id in self.imports:
            original_package = self.alias_to_original[node.id]
            self.usage[original_package].add(self.imports[node.id])
            
    def visit_Attribute(self, node):
        # Handle cases like torch.nn.Linear or alias.function
        if isinstance(node.value, ast.Name):
            base_name = node.value.id
            if base_name in self.imports:
                original_package = self.alias_to_original[base_name]
                full_attr = f"{self.imports[base_name]}.{node.attr}"
                self.usage[original_package].add(full_attr)
        self.generic_visit(node)

def analyze_python_files(directory):
    # Get all Python files in the directory
    python_files = []
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith('.py'):
                python_files.append(os.path.join(root, f))
    local_modules = {os.path.splitext(os.path.basename(f))[0] for f in python_files}
    
    all_usage = defaultdict(set)
    
    for file_path in python_files:
        try:
            tree = ast.parse(preprocess_python_file(file_path), filename=file_path)
            
            visitor = ImportUsageVisitor()
            visitor.visit(tree)
            
            # Merge usage, excluding local modules
            for package, uses in visitor.usage.items():
                if package not in local_modules:
                    if package == 'ast':
                        print(file_path)
                    filtered_uses = {use for use in uses if use != package}
                    if filtered_uses:  # Only add if there are remaining uses
                        all_usage[package].update(filtered_uses)
                    
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
    
    # Convert sets to sorted lists for better readability
    return {package: sorted(list(uses)) for package, uses in all_usage.items()}

# Usage example
if __name__ == "__main__":
    directory = "darts"  # Current directory, change as needed
    usage_dict = analyze_python_files(directory)
    
    # Print results
    for package, uses in usage_dict.items():
        print(f"\n{package}:")
        for use in uses:
            print(f"  - {use}")