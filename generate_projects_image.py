#!/usr/bin/env python3
"""
Convert the github_projects_table.html file to an image.
This script uses wkhtmltoimage to render the HTML and create a PNG.
"""

import os
import sys
import subprocess


def html_to_image(html_path: str, output_path: str) -> None:
    """Convert HTML file to PNG image using wkhtmltoimage."""
    
    # Get absolute path
    html_path = os.path.abspath(html_path)
    output_path = os.path.abspath(output_path)
    temp_output = output_path.replace('.png', '_temp.png')
    
    print(f"Converting {html_path} to {output_path}...")
    
    # Use wkhtmltoimage with options for better rendering
    cmd = [
        'wkhtmltoimage',
        '--width', '1400',
        '--quality', '95',
        '--enable-local-file-access',
        html_path,
        temp_output
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✓ Image generated")
        
        # Try to optimize the PNG with optipng if available
        try:
            optimize_cmd = ['optipng', '-o2', '-quiet', temp_output]
            subprocess.run(optimize_cmd, check=True, capture_output=True, text=True)
            print(f"✓ Image optimized")
        except (subprocess.CalledProcessError, FileNotFoundError):
            # If optipng is not available, just continue
            print(f"  (optipng not available, skipping optimization)")
        
        # Move temp file to final output
        os.rename(temp_output, output_path)
        
        # Get file size
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"✓ Image saved to {output_path} ({size_mb:.2f} MB)")
        
    except subprocess.CalledProcessError as e:
        print(f"Error converting HTML to image: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        if os.path.exists(temp_output):
            os.remove(temp_output)
        sys.exit(1)


def main():
    """Main function to convert HTML to image."""
    html_path = "github_projects_table.html"
    output_path = "github_projects_table.png"
    
    if not os.path.exists(html_path):
        print(f"Error: {html_path} not found!")
        sys.exit(1)
    
    html_to_image(html_path, output_path)
    print("Done!")


if __name__ == "__main__":
    main()
