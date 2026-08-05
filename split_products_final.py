import re
import os

def split_products_in_file(input_path, output_dir):
    """
    Reads a messy products.yml, splits it into chunks by ID, and saves new YAML files.
    """
    if not os.path.exists(input_path):
        print(f"Error: File {input_path} not found.")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Split content into individual product blocks.
    # We assume each product starts with a line containing '  - ' (list item)
    # We use a lookahead to keep the delimiter attached to the start of the block
    raw_blocks = re.split(r'(?=\n\s*-\s)', content)
    
    # Remove empty blocks
    raw_blocks = [block.strip() for block in raw_blocks if block.strip()]
    
    products = []
    
    for i, block in enumerate(raw_blocks):
        # Skip the very first block if it's just the 'products:' header
        if block.startswith('products:'):
            continue
            
        # Extract Fields using flexible regex
        # ID: Look for 'id: <number>' anywhere in the block
        id_match = re.search(r'id:\s*(\d+)', block)
        if not id_match:
            print(f"Warning: Product block {i} has no ID. Skipping.")
            continue
        prod_id = int(id_match.group(1))
        
        # Name: Look for 'name: "..." or name: ...'
        # We handle both quoted and unquoted names
        name_match = re.search(r'name:\s*"(.*?)"|name:\s*(.*?)(?:\n|$)', block, re.DOTALL)
        if name_match:
            # Group 1 is quoted, Group 2 is unquoted
            name = name_match.group(1) if name_match.group(1) else name_match.group(2)
            if name:
                name = name.strip()
            else:
                name = "Unknown Product"
        else:
            name = "Unknown Product"
            
        # Category: Look for 'category: ...'
        cat_match = re.search(r'category:\s*(.*?)(?:\n|$)', block)
        category = cat_match.group(1).strip() if cat_match else "Uncategorized"
        
        # Description: Look for 'description: ...'
        # This is tricky because description can be multi-line
        desc_match = re.search(r'description:\s*(.*?)(?:\n\s*#|\n\s*(?:[a-zA-Z_]+:|\n\s*-\s))', block, re.DOTALL)
        description = ""
        if desc_match:
            raw_desc = desc_match.group(1)
            # Clean up the description: replace multiple newlines with single spaces
            description = re.sub(r'\s+', ' ', raw_desc).strip()
            # Remove trailing quotes if present
            description = description.strip('"')
        else:
            description = ""
            
        products.append({
            'id': prod_id,
            'name': name,
            'category': category,
            'description': description
        })

    # Sort products by ID
    products.sort(key=lambda x: x['id'])
    print(f"Successfully parsed {len(products)} products.")

    # 2. Define Chunk Ranges
    # Chunk 1: 1-30
    # Chunk 2: 31-90
    # ...
    # Chunk 21: 601-611 (or remaining)
    chunks = []
    
    # Define ranges
    ranges = [
        (1, 30),
        (31, 90),
        (91, 120),
        (121, 150),
        (151, 180),
        (181, 210),
        (211, 240),
        (241, 270),
        (271, 300),
        (301, 330),
        (331, 360),
        (361, 390),
        (391, 420),
        (421, 450),
        (451, 480),
        (481, 510),
        (511, 540),
        (541, 570),
        (571, 600),
        (601, 611),
        (612, 10000) # Fallback for any remaining
    ]
    
    for chunk_num, (min_id, max_id) in enumerate(ranges, start=1):
        chunk_products = [p for p in products if min_id <= p['id'] <= max_id]
        
        if chunk_products:
            save_chunk(chunk_num, chunk_products, output_dir)
        else:
            print(f"Chunk {chunk_num}: No products in range {min_id}-{max_id}. Skipping.")

    print("All chunks created successfully.")

def save_chunk(chunk_num, products, output_dir):
    """
    Saves a list of products to a new YAML file with consistent formatting.
    """
    filepath = os.path.join(output_dir, f'products_chunk_{chunk_num}.yml')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("products:\n")
        for prod in products:
            # Escape any double quotes in values to ensure valid YAML
            safe_name = prod['name'].replace('"', '\\"')
            safe_category = prod['category'].replace('"', '\\"')
            safe_desc = prod['description'].replace('"', '\\"')
            
            f.write(f"- id: {prod['id']}\n")
            f.write(f'  name: "{safe_name}"\n')
            f.write(f'  category: "{safe_category}"\n')
            
            # Handle description: if it's long, use >- (folded scalar) for readability
            if len(safe_desc) > 50:
                f.write(f"  description: >-\n")
                # Split description into lines for better formatting
                words = safe_desc.split()
                line = ""
                for word in words:
                    if len(line) + len(word) + 1 > 80:  # 80 chars per line
                        f.write(f"    {line}\n")
                        line = word
                    else:
                        line = f"{line} {word}" if line else word
                if line:
                    f.write(f"    {line}\n")
            else:
                f.write(f'  description: "{safe_desc}"\n')
            
            f.write("\n")  # Empty line between products

    print(f"Created: {filepath} with {len(products)} products.")

if __name__ == '__main__':
    input_file = '_data/products.yml'
    output_directory = '_data'
    
    split_products_in_file(input_file, output_directory)

