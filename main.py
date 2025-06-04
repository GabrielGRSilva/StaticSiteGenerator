import os
import shutil
import sys
from src.htmlnode import *

def file_static_to_public(source_path="static", destination_path="docs"):

    #delete contents of docs before copying into it
    if source_path == "static":
        if os.path.exists(destination_path):
            shutil.rmtree(destination_path)
        os.mkdir(destination_path)

    items_in_source_path = os.listdir(f"{source_path}")
    for item in items_in_source_path:
        current_item_path = os.path.join(source_path, item)
        if os.path.isfile(current_item_path):
            shutil.copy(current_item_path, os.path.join(destination_path, item))
        elif os.path.isdir(current_item_path):
            new_dir = os.path.join(destination_path, item)
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            file_static_to_public(current_item_path, new_dir)


def extract_title(markdown):
    split_lines = markdown.split("\n")

    for line in split_lines:
        if line.startswith("# "):
            return line[2:].strip() #give me a new string starting from the 3rd character (index 2), all the way to the end.

    raise Exception("No header found")

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print (f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown_content = f.read()
    with open(template_path, "r") as f:
            template_content = f.read()
    html_string = markdown_to_html_node(markdown_content)
    processed_html_string = html_string.to_html()
    title = extract_title(markdown_content)
    title_content_replace = template_content.replace("{{ Title }}", title).replace("{{ Content }}", processed_html_string)
    href_replace = title_content_replace.replace('href="/', f'href="{basepath}')
    final_string = href_replace.replace('src="/', f'src="{basepath}')

    parent_dir = os.path.dirname(dest_path)
    os.makedirs(parent_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(final_string)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    paths = os.listdir(dir_path_content)
    for item in paths:
        path_to_item = os.path.join(dir_path_content, item)
        dest_path_to_item = os.path.join(dest_dir_path, item)
        if os.path.isfile(path_to_item):
            destination = os.path.splitext(dest_path_to_item)
            correct_extension = destination[0] + ".html"

            # This line ensures the destination directory exists
            os.makedirs(dest_dir_path, exist_ok=True)

            with open(path_to_item, "r") as f:
                markdown_content = f.read()
            with open(template_path, "r") as f:
                    template_content = f.read()
            html_string = markdown_to_html_node(markdown_content)
            processed_html_string = html_string.to_html()
            title = extract_title(markdown_content)
            title_content_replace = template_content.replace("{{ Title }}", title).replace("{{ Content }}", processed_html_string)
            href_replace = title_content_replace.replace('href="/', f'href="{basepath}')
            final_string = href_replace.replace('src="/', f'src="{basepath}')

            with open(correct_extension, "w") as f:
                f.write(final_string)

        else:
            new_dest_path = os.path.join(dest_dir_path, item)
            os.makedirs(new_dest_path, exist_ok=True)
    return ("Pages generated!")

def main():
    if len(sys.argv) >= 2:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    if os.path.exists("public"):
        shutil.rmtree("public")
    file_static_to_public()
    print ("Copying complete")
    generate_page("content/index.md", "template.html", "docs/index.html", basepath)
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main ()
