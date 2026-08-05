import re
import os

def load_products_from_messy_yaml(filepath):
    """
    Parses a messy YAML file where fields may be out of order or malformed.
    Extracts products based on the pattern: starts with '- name:' or '- id:'
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content into product blocks
    # We assume each product starts with '- name:' or '- id:'
    # We use a regex split that keeps the delimiter
    raw_products = re.split(r'\n(?=-\s*(?:name|id):)', content)
    
    products = []
    for block in raw_products:
        if not block.strip():
            continue
        
        # Extract fields using regex
        id_match = re.search(r'id:\s*(\d+)', block)
        name_match = re.search(r'name:\s*"?(.*?)"?\s*$', block, re.MULTILINE | re.DOTALL)
        category_match = re.search(r'category:\s*(.+)', block, re.MULTILINE | re.DOTALL)
        description_match = re.search(r'description:\s*(.*?)(?:\n\s*#|$|\n\s*(?:[a-zA-Z_]+:))', block, re.DOTALL)
        
        prod_id = int(id_match.group(1)) if id_match else -1
        name = name_match.group(1).strip() if name_match else "Unknown"
        category = category_match.group(1).strip() if category_match else "Uncategorized"
        
        desc_text = description_match.group(1).strip() if description_match else ""
        # Clean up description: remove extra whitespace and newlines
        desc_text = re.sub(r'\s+', ' ', desc_text).strip()
        
        products.append({
            'id': prod_id,
            'name': name,
            'category': category,
            'description': desc_text
        })
    
    return products

def save_chunk(chunk_id, products_list, output_dir):
    """
    Saves products to a clean YAML file with consistent formatting.
    """
    filepath = os.path.join(output_dir, f'products_chunk_{chunk_id}.yml')
    
    # Ensure product IDs are positive
    valid_products = [p for p in products_list if p['id'] > 0]
    
    if not valid_products:
        print(f"Chunk {chunk_id}: No valid products. Skipping.")
        return
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("products:\n")
        for prod in valid_products:
            f.write(f"- id: {prod['id']}\n")
            f.write(f'  name: "{prod['name']}"\n')
            f.write(f"  category: \"{prod['category']}\"\n")
            f.write(f"  description: >-\n")
            f.write(f"    {prod['description']}\n")
            f.write("\n")  # Empty line between products
    
    print(f"Created {filepath} with {len(valid_products)} products.")

def main():
    input_file = '_data/products.yml'
    output_dir = '_data'
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return
    
    print("Loading original products file...")
    products = load_products_from_messy_yaml(input_file)
    
    if not products:
        print("No products found. Check the file format.")
        return
    
    print(f"Loaded {len(products)} products.")
    
    # Sort by ID
    products.sort(key=lambda x: x['id'])
    
    # Define chunk ranges
    chunk_ranges = [
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
        (612, 1000)  # Fallback
    ]
    
    for i, (min_id, max_id) in enumerate(chunk_ranges, start=1):
        chunk_products = [p for p in products if min_id <= p['id'] <= max_id]
        save_chunk(i, chunk_products, output_dir)
    
    print("Done! All chunks created.")

if __name__ == '__main__':
    main()

