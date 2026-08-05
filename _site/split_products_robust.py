import re
import os

def split_into_product_blocks(content):
    """
    Splits the raw file content into individual product blocks.
    Assumes each product starts with '- ' and contains 'id:' or 'name:'
    """
    # Split by lines that start with '- ' and are followed by a key (like name:, id:, category:, description:)
    # We use a lookahead to ensure we split correctly
    pattern = r'\n(?=-\s+(?:name|id|category|description):)'
    
    # Split the content
    blocks = re.split(pattern, content)
    
    product_blocks = []
    for block in blocks:
        # Remove leading/trailing whitespace
        cleaned = block.strip()
        if not cleaned:
            continue
        product_blocks.append(cleaned)
    
    return product_blocks

def parse_product_block(block):
    """
    Parses a single product block and returns a dictionary.
    Handles out-of-order fields.
    """
    # Extract ID
    id_match = re.search(r'id:\s*(\d+)', block)
    prod_id = int(id_match.group(1)) if id_match else None
    
    # Extract Name
    name_match = re.search(r'name:\s*"?(.*?)"?\s*$', block, re.MULTILINE | re.DOTALL)
    name = name_match.group(1).strip() if name_match else "Unknown"
    
    # Extract Category
    cat_match = re.search(r'category:\s*(.+)', block, re.MULTILINE | re.DOTALL)
    category = cat_match.group(1).strip() if cat_match else "Uncategorized"
    
    # Extract Description
    # Description can be multi-line, so we capture everything until the next key or end
    desc_match = re.search(r'description:\s*(.*?)(?:\n\s*#|$|\n\s*(?:[a-zA-Z_]+:))', block, re.DOTALL)
    desc_text = desc_match.group(1).strip() if desc_match else ""
    # Clean up description: remove extra whitespace and newlines
    desc_text = re.sub(r'\s+', ' ', desc_text).strip()
    
    # Remove trailing quotes if present
    name = name.strip('"')
    category = category.strip('"')
    
    if prod_id is None:
        return None
    
    return {
        'id': prod_id,
        'name': name,
        'category': category,
        'description': desc_text
    }

def save_chunk(chunk_id, products_list, output_dir):
    """
    Saves products to a clean YAML file with consistent formatting.
    """
    filepath = os.path.join(output_dir, f'products_chunk_{chunk_id}.yml')
    
    # Filter valid products
    valid_products = [p for p in products_list if p['id'] > 0]
    
    if not valid_products:
        print(f"Chunk {chunk_id}: No valid products. Skipping.")
        return
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("products:\n")
        for prod in valid_products:
            # Escape any double quotes in name or category
            safe_name = prod['name'].replace('"', '\\"')
            safe_category = prod['category'].replace('"', '\\"')
            safe_desc = prod['description'].replace('"', '\\"')
            
            f.write(f"- id: {prod['id']}\n")
            f.write(f'  name: "{safe_name}"\n')
            f.write(f'  category: "{safe_category}"\n')
            f.write(f"  description: >-\n")
            # Indent description
            for line in safe_desc.split('. '):  # Simple sentence splitting for readability
                if line.strip():
                    f.write(f"    {line.strip()}.\n" if not line.strip().endswith('.') else f"    {line.strip()}\n")
            f.write("\n")  # Empty line between products
    
    print(f"Created {filepath} with {len(valid_products)} products.")

def main():
    input_file = '_data/products.yml'
    output_dir = '_data'
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return
    
    print("Reading original products file...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Splitting into product blocks...")
    blocks = split_into_product_blocks(content)
    print(f"Found {len(blocks)} product blocks.")
    
    if not blocks:
        print("No product blocks found. Check the file format.")
        return
    
    print("Parsing products...")
    all_products = []
    for i, block in enumerate(blocks):
        prod = parse_product_block(block)
        if prod:
            all_products.append(prod)
        else:
            print(f"Warning: Could not parse product block {i+1}")
    
    print(f"Successfully parsed {len(all_products)} products.")
    
    if not all_products:
        print("No valid products parsed.")
        return
    
    # Sort by ID
    all_products.sort(key=lambda x: x['id'])
    
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
        chunk_products = [p for p in all_products if min_id <= p['id'] <= max_id]
        save_chunk(i, chunk_products, output_dir)
    
    print("Done! All chunks created.")

if __name__ == '__main__':
    main()

