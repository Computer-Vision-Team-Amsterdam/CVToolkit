import logging
import os
import shutil

logger = logging.getLogger(__name__)


def delete_file(file_path):
    try:
        os.remove(file_path)
        logger.info(f"{file_path} has been deleted.")
    except FileNotFoundError:
        logger.error(f"{file_path} does not exist.")
    except Exception as e:
        logger.error(f"Failed to remove file '{file_path}': {str(e)}")
        raise Exception(f"Failed to remove file '{file_path}': {e}")


def copy_file(relative_path, input_path, output_path):
    # We don't use os.path.join because it doesn't work with Azure paths
    source_path = input_path + relative_path
    destination_path = output_path + relative_path

    logger.info(f"Copying {source_path} to {destination_path}..")
    if os.path.exists(source_path):
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        shutil.copy(source_path, destination_path)
        print(f"File '{source_path}' copied to '{destination_path}'")

        if not os.path.exists(destination_path):
            error_message = f"Failed to move file '{source_path}' to the destination: {destination_path}"
            logger.error(error_message)
            raise FileNotFoundError(error_message)
    else:
        logger.info(f"Source file '{source_path}' does not exist.")
