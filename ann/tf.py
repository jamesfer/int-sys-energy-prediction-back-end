import os
import tensorflow

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


tf = tensorflow


class VariableContainer:
    def __init__(self, variables):
        self.variables = variables
