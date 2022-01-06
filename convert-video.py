from tkinter import filedialog
from pathlib import Path
import mimetypes

import ffmpeg

# For now this just converts containers to .mp4
def ConvertFilesToMp4(folder: Path) -> None:
    # iterate through the files in the folder
    for file in folder.iterdir():
        # Check that file is actually a file and not hidden
        if file.is_file() and not file.name.startswith('.'):
            # Get the mimetype to check if it's a video format
            type = mimetypes.guess_type(file)[0]

            # If it is a video format
            if type is not None and type.startswith('video'):
                # Get the parent folder
                parent_folder = file.parent

                # Create the output forlder
                output_folder = parent_folder / 'converted'
                output_folder.mkdir(exist_ok=True)

                # Get the file extension stripping off the .
                file_ext = file.suffix.strip('.')

                # If this file isn't already a .mp4
                if file_ext != 'mp4':
                    (
                        ffmpeg
                        # Set the input
                        .input(file.as_posix())
                        # Set the output and ensure that the codecs are copied
                        .output(Path(output_folder / f'{file.stem}.mp4').as_posix(), **{'c':'copy'})
                        # Automatically overwrite any existing files
                        .overwrite_output()
                        # Run this asynchronously
                        .run_async()
                    )

# Main file entrypoint
if __name__ == '__main__':
    # Open a TkInter file dialog to request the folder to use
    folder = Path(filedialog.askdirectory(initialdir=Path.home()))

    # Convert the files in this folder
    ConvertFilesToMp4(folder)
