import enum


class ApplicationStates(enum.Enum):
    """
    Application states for the gui version
    """
    MAIN_MENU = 1
    SIGN_UP = 2
    LOGIN = 3
    ADD_SERVICE = 4
    CHECK_SERVICE = 5
    UPDATE_SERVICE = 6
    DELETE_SERVICE = 7
