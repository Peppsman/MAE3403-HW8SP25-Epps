#MAE 3403 P2 Rankine controller
#Copilet is my co-pilet

# Region: Imports
from PyQt5.QtWidgets import QApplication
from Rankine_Classes import RankineModel, RankineView, RankineController
import sys

# Region: Main Application
if __name__ == "__main__":
    """
    Entry point of the Rankine Cycle application.
    """
    app = QApplication(sys.argv)
    model = RankineModel()  # Create model instance
    view = RankineView()    # Create view instance
    controller = RankineController(model, view)  # Link Model and View via Controller
    view.show()
    sys.exit(app.exec_())
# End of Main Application