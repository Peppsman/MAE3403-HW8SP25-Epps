#MAE 3403 HW8P2 Epps, Patrick
#Copilet is good at dealing with fixing all my mistakes

# Region: Imports
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLineEdit, QLabel, QRadioButton

# Region: Model
class RankineModel:
    """
    Handles calculations and stores Rankine cycle data.
    """
    def __init__(self):
        self.units = "SI"  # Default unit system

    def getSaturationTemperature(self, P_high):
        """
        Returns the saturation temperature based on P High.
        Placeholder function with simple estimation.
        """
        return 100 + P_high * 2  # Mock calculation

    def getSaturationProperties(self, pressure):
        """
        Returns saturation properties for a given pressure.
        """
        return {"temperature": self.getSaturationTemperature(pressure)}

    def setUnits(self, unit_type):
        """
        Updates the unit system for calculations.
        """
        self.units = unit_type

# End of Model

# Region: View
class RankineView(QMainWindow):
    """
    Defines the graphical user interface for the Rankine Cycle.
    """
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Set up the GUI layout."""
        self.setWindowTitle('Rankine Cycle Viewer')

        # Set initial window size
        self.resize(600, 400)  # Width = 600px, Height = 400px

        self.layout = QVBoxLayout()

        # Add widgets...

        """
        Set up the GUI layout.
        """
        self.setWindowTitle('Rankine Cycle Viewer')
        self.layout = QVBoxLayout()

        # Inputs and buttons
        self.P_high_input = QLineEdit()
        self.P_low_input = QLineEdit()
        self.T_high_input = QLineEdit()
        self.radio_T_high = QRadioButton("Use T High")
        self.radio_SI = QRadioButton("SI Units")
        self.radio_English = QRadioButton("English Units")
        self.calculate_button = QPushButton("Calculate")

        # Labels for saturation properties
        self.label_sat_high = QLabel("Saturation High:")
        self.label_sat_low = QLabel("Saturation Low:")

        # Layout setup
        self.layout.addWidget(QLabel("P High (MPa):"))
        self.layout.addWidget(self.P_high_input)
        self.layout.addWidget(QLabel("P Low (MPa):"))
        self.layout.addWidget(self.P_low_input)
        self.layout.addWidget(self.radio_T_high)
        self.layout.addWidget(QLabel("Turbine Inlet Temp (°C):"))
        self.layout.addWidget(self.T_high_input)
        self.layout.addWidget(self.radio_SI)
        self.layout.addWidget(self.radio_English)
        self.layout.addWidget(self.label_sat_high)
        self.layout.addWidget(self.label_sat_low)
        self.layout.addWidget(self.calculate_button)

        central_widget = QLabel()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

# End of View

# Region: Controller
class RankineController:
    """
    Manages interactions between the Model and View for the Rankine Cycle.
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Connect UI actions to update functions
        self.view.radio_T_high.clicked.connect(self.updateTurbineInlet)
        self.view.P_high_input.editingFinished.connect(self.updateSaturationProperties)
        self.view.P_low_input.editingFinished.connect(self.updateSaturationProperties)
        self.view.radio_SI.clicked.connect(self.updateUnits)
        self.view.radio_English.clicked.connect(self.updateUnits)

    # Region: Update Turbine Inlet Temperature
    def updateTurbineInlet(self):
        """
        When 'T High' is selected, set Turbine Inlet Temp to saturation temperature at P High.
        """
        try:
            P_high = float(self.view.P_high_input.text())  # Get pressure input
            T_sat = self.model.getSaturationTemperature(P_high)  # Get corresponding temp
            self.view.T_high_input.setText(str(round(T_sat, 2)))  # Update UI
        except ValueError:
            print("ERROR: Invalid input for P High.")

    # Region: Update Saturation Properties
    def updateSaturationProperties(self):
        """
        Updates saturation labels when P High or P Low changes.
        Also updates T High if 'T High' is selected.
        """
        try:
            P_high = float(self.view.P_high_input.text())
            P_low = float(self.view.P_low_input.text())

            # Fetch saturation properties
            sat_high = self.model.getSaturationProperties(P_high)
            sat_low = self.model.getSaturationProperties(P_low)

            # Update UI labels
            self.view.label_sat_high.setText(f"Saturation High: {sat_high['temperature']} °C")
            self.view.label_sat_low.setText(f"Saturation Low: {sat_low['temperature']} °C")

            # If 'T High' is selected, update Turbine Inlet temperature
            if self.view.radio_T_high.isChecked():
                self.view.T_high_input.setText(str(round(sat_high['temperature'], 2)))

        except ValueError:
            print("ERROR: Invalid input for pressure values.")

    # Region: Update Units Immediately
    def updateUnits(self):
        """
        When the user selects SI or English units, immediately update labels and values.
        """
        unit_system = "SI" if self.view.radio_SI.isChecked() else "English"
        self.model.setUnits(unit_system)  # Update model units
        self.view.P_high_input.setPlaceholderText(f"Pressure High ({'MPa' if unit_system == 'SI' else 'psi'})")
        self.view.P_low_input.setPlaceholderText(f"Pressure Low ({'MPa' if unit_system == 'SI' else 'psi'})")
        self.view.T_high_input.setPlaceholderText(f"Turbine Inlet Temp ({'°C' if unit_system == 'SI' else '°F'})")

# End of Controller