class WorkspaceAgentException(Exception):

    """
    Base Exception
    """

    pass


class CameraException(WorkspaceAgentException):

    def __init__(self, message="Unable to access camera"):

        super().__init__(message)


class FaceDetectionException(WorkspaceAgentException):

    def __init__(self, message="Face detection failed"):

        super().__init__(message)


class EyeDetectionException(WorkspaceAgentException):

    def __init__(self, message="Eye detection failed"):

        super().__init__(message)


class PersonDetectionException(WorkspaceAgentException):

    def __init__(self, message="Person detection failed"):

        super().__init__(message)


class OllamaException(WorkspaceAgentException):

    def __init__(self, message="Unable to connect to Ollama"):

        super().__init__(message)


class DatabaseException(WorkspaceAgentException):

    def __init__(self, message="Database Error"):

        super().__init__(message)


class ReportException(WorkspaceAgentException):

    def __init__(self, message="Report Generation Failed"):

        super().__init__(message)