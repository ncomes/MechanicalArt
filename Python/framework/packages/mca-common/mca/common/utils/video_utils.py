"""
Modules that contains useful functions related to reprocessing video.
"""
# System global imports
import os
import subprocess
# mca python imports
from mca.common.project import paths
from mca.common import log

logger = log.MCA_LOGGER


def ffmpeg_convert_to_mp4(source_path):
    """
    Using command line and ffmpeg convert a video file to an mp4.

    :param str source_path: Path to a given video file.
    :return: Returns the path to the output file.
    :rtype: str
    """
    if not source_path or not os.path.isfile(source_path):
        raise IOError(f'{source_path} Source file not provided, or not on disk')

    processed_path = os.path.splitext(source_path)[0]+'.mp4'

    ffmpeg_exe_path = os.path.normpath(os.path.join(paths.get_common_tools_path(), r"3rdParty\FFmpeg\bin\ffmpeg.exe"))

    if not os.path.exists(ffmpeg_exe_path):
        raise IOError('Check your plastic configuration before continuing. Unable to find ffmpeg.exe.')

    if os.path.isfile(processed_path):
        # If the file exists ffmpeg will hang.  Deleting file first.
        try:
            os.remove(processed_path)
        except:
            raise IOError(f'{processed_path} Verify output file being overwritten is not read only.')

    execute_string = f'{os.path.normpath(ffmpeg_exe_path)} -i {os.path.normpath(source_path)} -c:v libx264 -crf 19 -preset slow -c:a aac -b:a 192k -ac 2 {os.path.normpath(processed_path)}'
    logger.debug(execute_string)
    subprocess.call(execute_string, shell=True)
    if os.path.isfile(processed_path):
        return processed_path
    else:
        raise FileNotFoundError(f'{source_path} Conversion failed, processed file was not found on disk.')
