class AutoTestBaseError(Exception):
    pass


class AppStartError(AutoTestBaseError):
    pass


class ElementNotFoundError(AutoTestBaseError):
    pass


class StepExecutionError(AutoTestBaseError):
    pass


class ConfigurationError(AutoTestBaseError):
    pass
