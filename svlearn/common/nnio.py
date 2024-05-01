
import logging

from svlearn.common.svexception import SVError
from svlearn.common.utils import *


# -----------------------------------------------------------------
def save_model(state_dict: dict, file_path: str) -> None:
    """
    Save the model to the file-system
    :param state_dict:
    :param file_path: full-path to the file to store it in
    :return: None
    """
    if not file_path:
        raise UnspecifiedFileError('file_path')
    path: Path = Path(file_path)
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    logging.info("Saving the model state-dictionary to the file: {file_path}")
    torch.save(state_dict, file_path)


# -----------------------------------------------------------------
def load_model(file_path: str) -> dict:
    """
    Save the model to the file-system
    :param state_dict:
    :param file_path: full-path to the file to store it in
    :return: a state-dictionary of the model
    """
    # pre-conditions check.
    if not file_path:
        raise UnspecifiedFileError('file_path')
    if not file_readable(file_path):
        raise SVError(f'The file path specified is not readable: {file_path}')

    logging.info("Loading the model state-dictionary from the file: {file_path}")
    return torch.load(file_path)
