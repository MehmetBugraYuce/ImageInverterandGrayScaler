import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageOps

def process_images():
    # 1. Setup the hidden GUI window
    root = tk.Tk()
    root.withdraw() # Hide the main empty window

    # 2. Ask user to select input files
    file_paths = filedialog.askopenfilenames(
        title="Select Images to Process",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]
    )

    if not file_paths:
        print("No files selected.")
        return

    # 3. Ask user for the output location
    output_dir = filedialog.askdirectory(title="Select Output Folder")
    
    if not output_dir:
        print("No output folder selected.")
        return

    # Create a specific folder for the results
    save_folder = os.path.join(output_dir, "Processed_Images")
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    count = 0

    # 4. Loop through images and process
    for file_path in file_paths:
        try:
            # Open the image
            with Image.open(file_path) as img:
                # Convert to RGB to ensure compatibility (e.g. handling PNG transparency)
                img_rgb = img.convert("RGB")
                
                # Step A: Invert the image
                inverted_img = ImageOps.invert(img_rgb)
                
                # Step B: Grayscale the inverted image
                final_img = inverted_img.convert("L")

                # Construct new filename
                # Get the original filename without extension (e.g., 'photo')
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                # Get the extension (e.g., '.jpg')
                ext = os.path.splitext(file_path)[1]
                
                new_name = f"{base_name}_inv_gs{ext}"
                save_path = os.path.join(save_folder, new_name)

                # Save the file
                final_img.save(save_path)
                count += 1
                print(f"Processed: {new_name}")

        except Exception as e:
            print(f"Failed to process {file_path}: {e}")

    # 5. Success Message
    messagebox.showinfo("Success", f"Finished! {count} images saved in:\n{save_folder}")

if __name__ == "__main__":
    process_images()