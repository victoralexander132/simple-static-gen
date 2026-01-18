import os
import sys
import shutil
from textnode import TextNode, TextType
from block_markdown import markdown_to_html_node, extract_title


def copy_directory_contents(src, dst):
    """
    Recursively copy all contents from source directory to destination directory.
    First deletes all contents of the destination directory to ensure a clean copy.
    """
    # Delete destination directory if it exists
    if os.path.exists(dst):
        print(f"Deleting destination directory: {dst}")
        shutil.rmtree(dst)
    
    # Create the destination directory
    print(f"Creating destination directory: {dst}")
    os.mkdir(dst)
    
    # Recursively copy contents
    _copy_recursive(src, dst)


def _copy_recursive(src, dst):
    """
    Helper function to recursively copy directory contents.
    """
    # List all items in the source directory
    items = os.listdir(src)
    
    for item in items:
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        
        if os.path.isfile(src_path):
            # Copy file
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            # Create directory and recursively copy its contents
            print(f"Creating directory: {dst_path}")
            os.mkdir(dst_path)
            _copy_recursive(src_path, dst_path)


def generate_page(from_path, template_path, dest_path, basepath="/"):
    """
    Generate an HTML page from a markdown file using a template.
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    # Read the template file
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract the title
    title = extract_title(markdown_content)
    
    # Replace placeholders in template
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    # Replace basepath in links and sources
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')
    
    # Create destination directory if it doesn't exist
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Write the final HTML to the destination file
    with open(dest_path, 'w') as f:
        f.write(final_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    """
    Recursively generate HTML pages for all markdown files in a directory.
    Maintains the same directory structure in the destination.
    """
    # List all entries in the content directory
    entries = os.listdir(dir_path_content)
    
    for entry in entries:
        src_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        
        if os.path.isfile(src_path):
            # If it's a markdown file, generate HTML
            if src_path.endswith('.md'):
                # Change .md extension to .html for destination
                html_dest_path = dest_path[:-3] + '.html'
                generate_page(src_path, template_path, html_dest_path, basepath)
        else:
            # If it's a directory, create it in destination and recurse
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            generate_pages_recursive(src_path, template_path, dest_path, basepath)


def main():
    # Get basepath from command line arguments, default to "/"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    print(f"Using basepath: {basepath}")
    
    # Copy static files to docs directory
    copy_directory_contents("static", "docs")
    print("\nStatic files copied successfully!")
    
    # Generate all pages recursively
    generate_pages_recursive("content", "template.html", "docs", basepath)
    print("\nAll pages generated successfully!")


if __name__ == "__main__":
    main()
