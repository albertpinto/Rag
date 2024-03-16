#  Copyright (c) 2020.  SupportVectors AI Lab
#  This code is part of the training material, and therefore part of the intellectual property.
#  It may not be reused or shared without the explicit, written permission of SupportVectors.
#
#  Use is limited to the duration and purpose of the training at SupportVectors.
#
#  Author: Asif Qamar
#
class SVError(Exception):
    def __init__(self, message=None):
        """
        Constructor
        :param message: the error message.
        """       
        self.message = message


# -----------------------------------------------------------------

class MissingArgumentError(SVError):

    def __init__(self, arg):
        """
         Attributes:
             arg: the name of the argument that is missing a value
         """
        self.message = f'A requirement argument: {arg} is missing!'


# -----------------------------------------------------------------

class UnspecifiedDirectoryError(SVError):
    """
    Exception raised when a required directory is not specified

    :param arg: the name of the argument that should contain the directory name
    :param message: explanation of the error

    """
    def __init__(self, arg, message=None):
        super.__init__(message)
        self.arg = arg
        if not self.message:
            self.message = f'Directory name must be specified for the arg: {self.arg}'


# -----------------------------------------------------------------

class UnspecifiedFileError(SVError):
    """
    Exception raised when a required file is not specified

    :param arg: the name of the argument that should contain
                    the file name
    :param message: explanation of the error
    :rtype: object
    
     """
    def __init__(self, arg, message=None):
        super.__init__(message)
        self.arg = arg
        if not self.message:
            self.message = f'File name must be specified for the arg: {self.arg}'



# -----------------------------------------------------------------


if __name__ == "__main__":
    """ Run the main if this module is run.
    """
    try:
        raise UnspecifiedDirectoryError(arg='xyzdir')
    except UnspecifiedDirectoryError as e:
        print(e.message)
