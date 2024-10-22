from PyQt6.QtCore import QThread, pyqtSignal
from Algorithm.DRT_Model  import DRT_Model

class DRT_Thread(QThread):
    result_ready = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.algorithm = DRT_Model()
        self.data = None
        
    def update_data(self, data):
        self.data = data

    def run(self):
        if self.data is not None:
            result = self.algorithm.run(self.data)
            self.result_ready.emit(result)
        else:
            print("No data provided for algorithm to run.")
        
