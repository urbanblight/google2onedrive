from logger import logger
import argparse
import os
import shutil

# SCENARIO: migrating from GoogleDrive to OneDrive
UNSUPPORTED_CHARACTERS = ['<', '>', ':', '"', '/', "\\", '|', '?', '*']
UNSUPPORTED_EXTENSIONS = ['Icon', '.DS_Store', '.gshortcut', '.gsheet',
                          '.gdoc']

logger.info("Using the following list as unsupported chars: {}".format(
    UNSUPPORTED_CHARACTERS))
logger.info("Using the following list as unsupported extensions: {}".format(
    UNSUPPORTED_EXTENSIONS))


def onedrive_clean(fn):
    """ Removes  characters unsafe for OneDrive from string """
    for unsupported_char in UNSUPPORTED_CHARACTERS:
        # remove the character from the path
        new_path = fn.translate({ord(unsupported_char): None})
    return new_path


def onedrive_safe(fn):
    """ Returns false for file names that unsafe for OneDrive """
    for s in UNSUPPORTED_EXTENSIONS:
        if s in fn:
            return False
    return True


def loop_dir(local_path, onedrive_path, midstring=''):
    """ Recurses through dirs and copies """
    for fn in os.listdir(local_path):
        if onedrive_safe(fn):
            src = os.path.join(local_path, fn)
            if not os.path.isdir(src):
                # Make destination path safe for OneDrive
                dst = onedrive_path + onedrive_clean(fn) if midstring == '' \
                    else onedrive_path + midstring + '/' + onedrive_clean(fn)
                logger.info("Copying to: {}".format(dst))
                # Execute the copy
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy(src, dst)
            else:
                logger.debug("Recursing directory: {}".format({src}))
                loop_dir(src, onedrive_path,
                         fn if midstring == '' else midstring + '/' + fn)
        else:
            logger.debug('skipping GoogleDrive file: {}'.format(fn))


if __name__ == "__main__":

    # Command line arguments
    parser = argparse.ArgumentParser(
        description='Copies folder recursively with safe names for OneDrive.')
    parser.add_argument('local_path', type=str,
                        help="full path to local folder to be copied")
    parser.add_argument('oneDrive_path', type=str,
                        help="full path to local OneDrive folder to create")
    args = parser.parse_args()

    loop_dir(args.local_path, args.oneDrive_path)
