import os
import subprocess
import platform
import shutil

def move_to_trash(file_path):
    """Move file to trash/recycle bin depending on the OS"""
    system = platform.system()
    
    try:
        if system == "Darwin":  # macOS
            subprocess.run(['osascript', '-e', f'tell application "Finder" to delete POSIX file "{file_path}"'], check=True)
        elif system == "Windows":
            # For Windows, we'll use send2trash if available, otherwise just delete
            try:
                import send2trash
                send2trash.send2trash(file_path)
            except ImportError:
                # Fallback: move to recycle bin using powershell
                subprocess.run(['powershell', '-command', f'Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile("{file_path}", "OnlyErrorDialogs", "SendToRecycleBin")'], check=True)
        elif system == "Linux":
            # For Linux, try to use gio trash command
            subprocess.run(['gio', 'trash', file_path], check=True)
        else:
            print(f"Unsupported OS: {system}. File will not be moved to trash.")
            return False
        
        print(f"Moved to trash: {file_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error moving {file_path} to trash: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error moving {file_path} to trash: {e}")
        return False

def get_video_height(file_path):
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=height', '-of', 'default=nw=1:nk=1', file_path],
            stdout=subprocess.PIPE,
            text=True,
            check=True
        )
        height_str = result.stdout.strip()
        if height_str:
            return int(height_str)
        else:
            return None
    except subprocess.CalledProcessError:
        return None
    except ValueError:
        return None

def process_video(file_path):
    height = get_video_height(file_path)
    if height is None:
        print(f"Skipping {file_path}: Not a valid video or error occurred.")
        return

    if height <= 720:
        print(f"Leaving {file_path} as is (height: {height}).")
        return

    # Resize if larger
    base_name = os.path.splitext(file_path)[0]
    extension = os.path.splitext(file_path)[1]
    output_path = base_name + '_720.mp4'
    
    # Check if output file already exists
    if os.path.exists(output_path):
        print(f"Output file {output_path} already exists. Skipping conversion.")
        return
    
    cmd = [
        'ffmpeg', '-i', file_path,
        '-vf', 'scale=-2:720',
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', 'experimental',  # In case needed for aac
        output_path
    ]
    
    try:
        print(f"Converting {file_path} to {output_path}...")
        subprocess.run(cmd, check=True)
        print(f"Successfully processed {file_path} to {output_path} (original height: {height}).")
        
        # Verify the output file was created successfully
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            # Move original file to trash
            if move_to_trash(file_path):
                print(f"Original file moved to trash: {file_path}")
            else:
                print(f"Warning: Could not move original file to trash: {file_path}")
        else:
            print(f"Error: Output file {output_path} was not created properly. Keeping original file.")
            
    except subprocess.CalledProcessError as e:
        print(f"Error processing {file_path}: {e}")

def main():
    root_dir = '/Volumes/Без названия/Edu/Youtube'
    video_extensions = {'.mp4', '.mov', '.mkv', '.avi', '.webm', '.flv', '.wmv'}

    if not os.path.exists(root_dir):
        print(f"Error: Directory {root_dir} does not exist.")
        return

    print(f"Starting video processing in: {root_dir}")
    print("Files with height > 720 will be converted to 720p and originals moved to trash.")
    print("-" * 60)

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if os.path.splitext(file)[1].lower() in video_extensions:
                full_path = os.path.join(subdir, file)
                process_video(full_path)

    print("-" * 60)
    print("Video processing completed.")

if __name__ == '__main__':
    main()