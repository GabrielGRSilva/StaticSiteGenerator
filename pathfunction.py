import os
import shutil

def file_static_to_public(source_path="root/static", destination_path="root/public"):
    items_in_source_path = os.listdir(f"{source_path}")

    #delete contents of public before copying into it
    if source_path == "root/static":
        shutil.rmtree(destination_path)
        os.mkdir(destination_path)

    for item in items_in_source_path:
        current_item_path = os.path.join(source_path, item)
        if os.path.isfile(current_item_path):
            shutil.copy(current_item_path, os.path.join(destination_path, item))
        elif os.path.exists(current_item_path):
            new_dir = os.path.join(destination_path, item)
            os.mkdir(new_dir)
            file_static_to_public(current_item_path, new_dir)
        else:
            print ("Copying complete")
