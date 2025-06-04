#!/usr/bin/env python3
"""
Image Processor - Batch Resize & Convert to WebP
A GUI application for batch image processing with resizing and WebP conversion capabilities.

Author: Jericho
License: MIT
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image, ImageTk
import threading
from pathlib import Path
import time
import sys


class ImageProcessor:
    """Main application class for the Image Processor."""

    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor - Batch Resize & Convert to WebP")
        self.root.geometry("900x750")
        self.root.minsize(800, 600)

        # Variables
        self.input_files = []
        self.output_path = tk.StringVar()
        self.width = tk.IntVar(value=800)
        self.height = tk.IntVar(value=600)
        self.quality = tk.IntVar(value=80)
        self.crop_enabled = tk.BooleanVar()
        self.maintain_aspect = tk.BooleanVar(value=True)
        self.add_suffix = tk.BooleanVar(value=True)
        self.suffix = tk.StringVar(value="_processed")

        # New variable for conversion mode
        self.convert_only = tk.BooleanVar(value=False)

        # Progress variables
        self.progress_var = tk.DoubleVar()
        self.current_file_var = tk.StringVar()
        self.processing = False

        self.create_widgets()

    def create_widgets(self):
        """Create and layout all GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Input files selection
        input_frame = ttk.LabelFrame(main_frame, text="Input Images", padding="5")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)

        # File selection buttons
        buttons_frame = ttk.Frame(input_frame)
        buttons_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))

        ttk.Button(buttons_frame, text="Select Files", command=self.select_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Select Folder", command=self.select_folder).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Clear List", command=self.clear_files).pack(side=tk.LEFT)

        # Files list
        list_frame = ttk.Frame(input_frame)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        input_frame.rowconfigure(1, weight=1)

        self.files_listbox = tk.Listbox(list_frame, height=6)
        self.files_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.files_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.files_listbox.configure(yscrollcommand=scrollbar.set)

        # Processing mode
        mode_frame = ttk.LabelFrame(main_frame, text="Processing Mode", padding="5")
        mode_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Radiobutton(mode_frame, text="Resize and convert to WebP",
                        variable=self.convert_only, value=False,
                        command=self.toggle_resize_options).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        ttk.Radiobutton(mode_frame, text="Convert to WebP only (keep original size)",
                        variable=self.convert_only, value=True,
                        command=self.toggle_resize_options).grid(row=1, column=0, sticky=tk.W)

        # Processing parameters
        self.params_frame = ttk.LabelFrame(main_frame, text="Processing Parameters", padding="5")
        self.params_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # Dimensions
        self.size_frame = ttk.Frame(self.params_frame)
        self.size_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))

        ttk.Label(self.size_frame, text="Width:").grid(row=0, column=0, sticky=tk.W)
        self.width_entry = ttk.Entry(self.size_frame, textvariable=self.width, width=10)
        self.width_entry.grid(row=0, column=1, padx=(5, 15))

        ttk.Label(self.size_frame, text="Height:").grid(row=0, column=2, sticky=tk.W)
        self.height_entry = ttk.Entry(self.size_frame, textvariable=self.height, width=10)
        self.height_entry.grid(row=0, column=3, padx=(5, 0))

        # Options
        self.options_frame = ttk.Frame(self.params_frame)
        self.options_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))

        self.maintain_aspect_cb = ttk.Checkbutton(self.options_frame, text="Maintain aspect ratio",
                                                  variable=self.maintain_aspect)
        self.maintain_aspect_cb.grid(row=0, column=0, sticky=tk.W)

        self.crop_enabled_cb = ttk.Checkbutton(self.options_frame, text="Center crop",
                                               variable=self.crop_enabled)
        self.crop_enabled_cb.grid(row=0, column=1, sticky=tk.W, padx=(20, 0))

        # WebP quality
        quality_frame = ttk.Frame(self.params_frame)
        quality_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))

        ttk.Label(quality_frame, text="WebP Quality:").grid(row=0, column=0, sticky=tk.W)
        ttk.Scale(quality_frame, from_=1, to=100, orient=tk.HORIZONTAL,
                  variable=self.quality, length=200).grid(row=0, column=1, padx=(5, 5))
        ttk.Label(quality_frame, textvariable=self.quality).grid(row=0, column=2)

        # File naming settings
        naming_frame = ttk.Frame(self.params_frame)
        naming_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))

        ttk.Checkbutton(naming_frame, text="Add suffix:",
                        variable=self.add_suffix).grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(naming_frame, textvariable=self.suffix, width=15).grid(row=0, column=1, padx=(5, 0))

        # Output folder
        output_frame = ttk.LabelFrame(main_frame, text="Output Folder", padding="5")
        output_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(0, weight=1)

        ttk.Entry(output_frame, textvariable=self.output_path).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(output_frame, text="Select Folder", command=self.select_output_folder).grid(row=0, column=1)

        # Processing progress
        progress_frame = ttk.LabelFrame(main_frame, text="Processing Progress", padding="5")
        progress_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)

        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                            maximum=100, length=400)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))

        ttk.Label(progress_frame, textvariable=self.current_file_var).grid(row=1, column=0, sticky=tk.W)

        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(0, 10))

        self.process_button = ttk.Button(button_frame, text="Process All",
                                         command=self.process_images)
        self.process_button.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(button_frame, text="Preview", command=self.preview_image).pack(side=tk.LEFT, padx=(0, 10))

        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_processing, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT)

        # Preview area
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="5")
        preview_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.rowconfigure(6, weight=1)

        self.preview_label = ttk.Label(preview_frame, text="Select images to preview")
        self.preview_label.pack(expand=True)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

    def toggle_resize_options(self):
        """Enable/disable resize options based on processing mode."""
        if self.convert_only.get():
            # Disable resize elements
            self.width_entry.configure(state='disabled')
            self.height_entry.configure(state='disabled')
            self.maintain_aspect_cb.configure(state='disabled')
            self.crop_enabled_cb.configure(state='disabled')
        else:
            # Enable resize elements
            self.width_entry.configure(state='normal')
            self.height_entry.configure(state='normal')
            self.maintain_aspect_cb.configure(state='normal')
            self.crop_enabled_cb.configure(state='normal')

    def select_files(self):
        """Select individual files."""
        filenames = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                ("Images", "*.jpg *.jpeg *.png *.bmp *.tiff *.gif *.webp"),
                ("All files", "*.*")
            ]
        )

        for filename in filenames:
            if filename not in self.input_files:
                self.input_files.append(filename)

        self.update_files_list()

    def select_folder(self):
        """Select folder with images."""
        folder = filedialog.askdirectory(title="Select folder with images")
        if folder:
            extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif', '.webp'}

            for file_path in Path(folder).rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in extensions:
                    file_str = str(file_path)
                    if file_str not in self.input_files:
                        self.input_files.append(file_str)

            self.update_files_list()

            # Automatically set output folder
            if not self.output_path.get():
                self.output_path.set(folder)

    def clear_files(self):
        """Clear files list."""
        self.input_files.clear()
        self.update_files_list()

    def update_files_list(self):
        """Update files list in GUI."""
        self.files_listbox.delete(0, tk.END)
        for file_path in self.input_files:
            filename = os.path.basename(file_path)
            self.files_listbox.insert(tk.END, filename)

        self.status_var.set(f"Selected files: {len(self.input_files)}")

    def select_output_folder(self):
        """Select output folder."""
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_path.set(folder)

    def resize_image(self, image, target_width, target_height, maintain_aspect, crop_enabled):
        """Resize image according to settings."""
        original_width, original_height = image.size

        if maintain_aspect and not crop_enabled:
            # Scale with aspect ratio preservation
            ratio = min(target_width / original_width, target_height / original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        elif maintain_aspect and crop_enabled:
            # Scale and crop
            ratio = max(target_width / original_width, target_height / original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)

            # First scale
            resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Then crop from center
            left = (new_width - target_width) // 2
            top = (new_height - target_height) // 2
            right = left + target_width
            bottom = top + target_height

            return resized.crop((left, top, right, bottom))

        else:
            # Simple resize without aspect ratio preservation
            return image.resize((target_width, target_height), Image.Resampling.LANCZOS)

    def preview_image(self):
        """Show preview of processed image."""
        if not self.input_files:
            messagebox.showwarning("Warning", "Select images first")
            return

        # Use first file from list for preview
        selected_indices = self.files_listbox.curselection()
        file_index = selected_indices[0] if selected_indices else 0

        try:
            # Load image
            with Image.open(self.input_files[file_index]) as img:
                if self.convert_only.get():
                    # Only conversion, keep size
                    processed = img.copy()
                else:
                    # Process image
                    processed = self.resize_image(
                        img, self.width.get(), self.height.get(),
                        self.maintain_aspect.get(), self.crop_enabled.get()
                    )

                # Scale for preview (max 400x300)
                preview_size = (400, 300)
                preview_img = processed.copy()
                preview_img.thumbnail(preview_size, Image.Resampling.LANCZOS)

                # Convert for tkinter
                photo = ImageTk.PhotoImage(preview_img)

                # Update preview
                self.preview_label.configure(image=photo, text="")
                self.preview_label.image = photo  # Keep reference

                filename = os.path.basename(self.input_files[file_index])
                if self.convert_only.get():
                    status_text = f"Preview: {filename} - {processed.size[0]}x{processed.size[1]} (conversion only)"
                else:
                    status_text = f"Preview: {filename} - {processed.size[0]}x{processed.size[1]} (with resize)"

                self.status_var.set(status_text)

        except Exception as e:
            messagebox.showerror("Error", f"Preview error: {str(e)}")

    def generate_output_filename(self, input_path, output_dir):
        """Generate output filename."""
        base_name = os.path.splitext(os.path.basename(input_path))[0]

        if self.add_suffix.get():
            filename = f"{base_name}{self.suffix.get()}.webp"
        else:
            filename = f"{base_name}.webp"

        return os.path.join(output_dir, filename)

    def stop_processing(self):
        """Stop processing."""
        self.processing = False

    def process_images_thread(self):
        """Process images in separate thread."""
        try:
            if not self.input_files:
                messagebox.showwarning("Warning", "Select images to process")
                return

            output_dir = self.output_path.get()
            if not output_dir:
                messagebox.showwarning("Warning", "Select output folder")
                return

            # Create output folder if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)

            self.processing = True
            total_files = len(self.input_files)
            processed_count = 0
            failed_files = []

            # Update interface
            self.process_button.configure(state=tk.DISABLED)
            self.stop_button.configure(state=tk.NORMAL)

            for i, input_file in enumerate(self.input_files):
                if not self.processing:
                    break

                try:
                    filename = os.path.basename(input_file)
                    self.current_file_var.set(f"Processing: {filename}")

                    # Generate output filename
                    output_file = self.generate_output_filename(input_file, output_dir)

                    # Open and process image
                    with Image.open(input_file) as img:
                        # Convert to RGB if necessary
                        if img.mode in ('RGBA', 'LA', 'P'):
                            img = img.convert('RGB')

                        if self.convert_only.get():
                            # Only convert to WebP, keep size
                            processed = img
                        else:
                            # Resize
                            processed = self.resize_image(
                                img, self.width.get(), self.height.get(),
                                self.maintain_aspect.get(), self.crop_enabled.get()
                            )

                        # Save as WebP
                        processed.save(output_file, 'WebP', quality=self.quality.get(), optimize=True)

                    processed_count += 1

                except Exception as e:
                    failed_files.append(f"{filename}: {str(e)}")

                # Update progress
                progress = ((i + 1) / total_files) * 100
                self.progress_var.set(progress)

                # Small pause for interface update
                time.sleep(0.01)

            # Processing completion
            self.processing = False
            self.process_button.configure(state=tk.NORMAL)
            self.stop_button.configure(state=tk.DISABLED)

            if self.processing is False and processed_count < total_files:
                self.current_file_var.set("Processing stopped by user")
                self.status_var.set(f"Stopped. Processed: {processed_count}/{total_files}")
            else:
                self.current_file_var.set("Processing completed")
                self.status_var.set(f"Done! Processed: {processed_count}/{total_files}")

            # Show results
            if failed_files:
                error_msg = f"Processed: {processed_count}/{total_files}\n\nErrors:\n" + "\n".join(failed_files[:10])
                if len(failed_files) > 10:
                    error_msg += f"\n... and {len(failed_files) - 10} more files"
                messagebox.showwarning("Completed with errors", error_msg)
            else:
                mode_text = "converted" if self.convert_only.get() else "processed"
                messagebox.showinfo("Success",
                                    f"All images successfully {mode_text}!\nProcessed: {processed_count}/{total_files}\nSaved to: {output_dir}")

        except Exception as e:
            self.processing = False
            self.process_button.configure(state=tk.NORMAL)
            self.stop_button.configure(state=tk.DISABLED)
            self.status_var.set("Processing error")
            messagebox.showerror("Error", f"Critical error: {str(e)}")

    def process_images(self):
        """Start batch image processing."""
        if self.processing:
            return

        thread = threading.Thread(target=self.process_images_thread)
        thread.daemon = True
        thread.start()


def main():
    """Main function to run the application."""
    try:
        root = tk.Tk()
        app = ImageProcessor(root)

        # Center window on screen
        root.update_idletasks()
        x = (root.winfo_screenwidth() - root.winfo_width()) // 2
        y = (root.winfo_screenheight() - root.winfo_height()) // 2
        root.geometry(f"+{x}+{y}")

        root.mainloop()
    except Exception as e:
        messagebox.showerror("Startup Error", f"Failed to start application: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()