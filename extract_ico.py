#!/usr/bin/env python3
import os
import sys
import subprocess
import struct
import tempfile
import shutil
try:
    from PIL import Image # type: ignore
except ImportError:
    print("Required packages not found. Install with:")
    print("pip install pillow")
    sys.exit(1)

def extract_icon_with_icoutils(exe_path, output_path):
    """Extract icon using icoutils (wrestool + icotool)"""
    try:
        # First, try to extract resources using wrestool
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract all icon resources
            cmd = ['wrestool', '-x', '--type=14', exe_path]  # Type 14 is RT_GROUP_ICON
            result = subprocess.run(cmd, capture_output=True, cwd=temp_dir)
            
            if result.returncode != 0:
                # Try extracting individual icons (Type 3)
                cmd = ['wrestool', '-x', '--type=3', exe_path]
                result = subprocess.run(cmd, capture_output=True, cwd=temp_dir)
            
            if result.returncode == 0:
                # Look for extracted .ico files
                ico_files = [f for f in os.listdir(temp_dir) if f.endswith('.ico')]
                if ico_files:
                    # Copy the first icon found
                    shutil.copy(os.path.join(temp_dir, ico_files[0]), output_path)
                    return os.path.exists(output_path) and os.path.getsize(output_path) > 100
                
                # If no .ico files, try to convert raw resources with icotool
                raw_files = [f for f in os.listdir(temp_dir) if not f.endswith('.ico')]
                for raw_file in raw_files:
                    try:
                        cmd = ['icotool', '-x', os.path.join(temp_dir, raw_file)]
                        subprocess.run(cmd, capture_output=True, cwd=temp_dir)
                        
                        # Look for generated PNG files and convert to ICO
                        png_files = [f for f in os.listdir(temp_dir) if f.endswith('.png')]
                        if png_files:
                            # Convert first PNG to ICO using PIL
                            img = Image.open(os.path.join(temp_dir, png_files[0]))
                            img.save(output_path, format='ICO')
                            return os.path.exists(output_path) and os.path.getsize(output_path) > 100
                    except:
                        continue
        
        return False
    except Exception as e:
        print(f"icoutils extraction failed: {str(e)}")
        return False

def extract_icon_with_objdump(exe_path, output_path):
    """Extract icon using objdump and manual parsing"""
    try:
        # Use objdump to get section information
        cmd = ['objdump', '-h', exe_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return False
        
        # Look for .rsrc section (Windows PE resources in Wine executables)
        rsrc_info = None
        for line in result.stdout.split('\n'):
            if '.rsrc' in line:
                parts = line.split()
                if len(parts) >= 6:
                    try:
                        size = int(parts[2], 16)
                        offset = int(parts[5], 16)
                        rsrc_info = (offset, size)
                        break
                    except:
                        continue
        
        if not rsrc_info:
            return False
        
        # Read the resource section
        with open(exe_path, 'rb') as f:
            f.seek(rsrc_info[0])
            rsrc_data = f.read(rsrc_info[1])
        
        # Simple heuristic: look for ICO signature (00 00 01 00)
        ico_signature = b'\x00\x00\x01\x00'
        pos = rsrc_data.find(ico_signature)
        
        if pos != -1:
            # Try to extract what looks like an ICO file
            # Read ICO header to determine size
            if pos + 6 < len(rsrc_data):
                num_images = struct.unpack('<H', rsrc_data[pos+4:pos+6])[0]
                if num_images > 0 and num_images < 20:  # Reasonable number of images
                    # Estimate ICO size (header + directory entries + image data)
                    estimated_size = 6 + (num_images * 16) + (num_images * 1024)  # Conservative estimate
                    ico_data = rsrc_data[pos:pos+min(estimated_size, len(rsrc_data)-pos)]
                    
                    with open(output_path, 'wb') as f:
                        f.write(ico_data)
                    
                    # Verify it's a valid ICO by trying to open with PIL
                    try:
                        img = Image.open(output_path)
                        img.verify()
                        return True
                    except:
                        os.remove(output_path)
        
        return False
    except Exception as e:
        print(f"objdump extraction failed: {str(e)}")
        return False

def extract_icon_from_desktop_file(exe_path, output_path):
    """Try to find icon from .desktop files or system icons"""
    try:
        # Get the basename of the executable
        exe_name = os.path.basename(exe_path).lower()
        exe_name_no_ext = os.path.splitext(exe_name)[0]
        
        # Common icon directories
        icon_dirs = [
            '/usr/share/icons',
            '/usr/share/pixmaps',
            os.path.expanduser('~/.local/share/icons'),
            '/usr/local/share/icons'
        ]
        
        # Common icon extensions
        icon_exts = ['.png', '.svg', '.xpm', '.ico']
        
        # Search for matching icons
        for icon_dir in icon_dirs:
            if not os.path.exists(icon_dir):
                continue
                
            for root, dirs, files in os.walk(icon_dir):
                for file in files:
                    file_lower = file.lower()
                    file_no_ext = os.path.splitext(file_lower)[0]
                    
                    if (file_no_ext == exe_name_no_ext or 
                        exe_name_no_ext in file_no_ext or 
                        file_no_ext in exe_name_no_ext):
                        
                        icon_path = os.path.join(root, file)
                        try:
                            # Convert to ICO format
                            img = Image.open(icon_path)
                            # Resize to standard icon size if needed
                            if img.size != (32, 32):
                                img = img.resize((32, 32), Image.Resampling.LANCZOS)
                            img.save(output_path, format='ICO')
                            return os.path.exists(output_path) and os.path.getsize(output_path) > 100
                        except:
                            continue
        
        return False
    except Exception as e:
        print(f"Desktop file icon search failed: {str(e)}")
        return False

def extract_icon_with_strings(exe_path, output_path):
    """Use strings command to find embedded icon paths"""
    try:
        cmd = ['strings', exe_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return False
        
        # Look for icon-related paths in strings output
        for line in result.stdout.split('\n'):
            line_lower = line.lower()
            if any(ext in line_lower for ext in ['.ico', '.png', '.xpm']) and '/' in line:
                # Found a potential icon path
                if os.path.exists(line.strip()):
                    try:
                        img = Image.open(line.strip())
                        img.save(output_path, format='ICO')
                        return os.path.exists(output_path) and os.path.getsize(output_path) > 100
                    except:
                        continue
        
        return False
    except Exception as e:
        print(f"strings extraction failed: {str(e)}")
        return False

def create_default_icon(output_path):
    """Create a default icon if extraction fails"""
    try:
        # Create a simple default icon using PIL
        img = Image.new('RGBA', (32, 32), color=(64, 64, 64, 255))
        
        # Draw a simple executable icon (folder-like shape)
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        
        # Draw a simple document/executable icon
        draw.rectangle([4, 6, 28, 28], fill=(128, 128, 128, 255), outline=(0, 0, 0, 255))
        draw.rectangle([6, 8, 26, 26], fill=(200, 200, 200, 255))
        draw.rectangle([8, 10, 24, 12], fill=(64, 64, 64, 255))
        draw.rectangle([8, 14, 20, 16], fill=(64, 64, 64, 255))
        draw.rectangle([8, 18, 22, 20], fill=(64, 64, 64, 255))
        
        # Save as ICO
        img.save(output_path, format='ICO')
        
        print(f"Created default icon at {output_path}")
        return os.path.exists(output_path)
    except Exception as e:
        print(f"Default icon creation failed: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_icon.py <exe_path> <output_ico>")
        sys.exit(1)
    
    exe_path = sys.argv[1]
    output_path = sys.argv[2]
    
    if not os.path.exists(exe_path):
        print(f"Error: File {exe_path} does not exist")
        sys.exit(1)
    
    # Try different extraction methods in order of preference
    methods = [
        ("icoutils (wrestool/icotool)", extract_icon_with_icoutils),
        ("objdump resource parsing", extract_icon_with_objdump),
        ("system icon search", extract_icon_from_desktop_file),
        ("strings analysis", extract_icon_with_strings)
    ]
    
    for method_name, method_func in methods:
        print(f"Trying {method_name}...")
        if method_func(exe_path, output_path):
            print(f"Successfully extracted icon to {output_path} using {method_name}")
            sys.exit(0)
    
    # Create a default icon as last resort
    if create_default_icon(output_path):
        print(f"Created default icon at {output_path}")
    else:
        print(f"Failed to extract icon from {exe_path}")
        sys.exit(1)