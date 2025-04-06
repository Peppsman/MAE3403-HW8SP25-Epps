#MAE 3403 HW8P1 Epps, Patrick
#Copilet is good, dealing with fixing all my mistakes

# Imports
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QLabel, QWidget

# MVC Structure

# Region: Model
class PumpModel:
    """
    The Model: Handles data processing and mathematical operations.
    """
    def __init__(self):
        self.file_path = None
        self.data = {'Flow Rate': [], 'Head': [], 'Efficiency': []}

    def set_file_path(self, path):
        """Store the file path."""
        self.file_path = path
#PBE needs to undersatnd the txt file
    def load_data(self):
        """
        Load and parse the text file.
        Assumes each line contains: Flow Rate, Head, Efficiency (space-separated).
        """
        if not self.file_path:
            raise ValueError("File path not set!")

        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    print(f"DEBUG: Reading line - {line.strip()}")  # Add this debug print
                    values = line.strip().split()  # Split values by whitespace
                    if len(values) == 3:  # Ensure correct format
                        try:
                            flow, head, eff = map(float, values)
                            self.data['Flow Rate'].append(flow)
                            self.data['Head'].append(head)
                            self.data['Efficiency'].append(eff)
                        except ValueError:
                            print(f"ERROR: Could not convert line {line.strip()} to float values.")
                    else:
                        print(f"WARNING: Unexpected format in line - {line.strip()}")
        except Exception as e:
            print(f"ERROR: File reading issue - {e}")

    def fit_quadratic_head(self):
        """Fit a quadratic curve to the Head data and return coefficients."""
        coeffs = np.polyfit(self.data['Flow Rate'], self.data['Head'], 2)
        return coeffs

    def fit_cubic_efficiency(self):
        """Fit a cubic curve to the Efficiency data and return coefficients."""
        coeffs = np.polyfit(self.data['Flow Rate'], self.data['Efficiency'], 3)
        return coeffs

# End of Model

# Region: View
#PBE better UI
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class PumpView(QWidget):
    """
    The View: Defines the GUI layout and components.
    """

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Set up the GUI layout."""
        self.setWindowTitle('Pump File Viewer')
        self.layout = QVBoxLayout()

        # Button to read file and calculate
        self.read_button = QPushButton('Read File and Calculate')

        # Table for displaying data
        self.table = QTableWidget()
        self.table.setColumnCount(3)  # Flow Rate, Head, Efficiency
        self.table.setHorizontalHeaderLabels(['Flow Rate', 'Head', 'Efficiency'])

        # Button to process edited data
        self.process_button = QPushButton('Update & Plot')

        # Add widgets to layout
        self.layout.addWidget(self.read_button)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.process_button)

        self.setLayout(self.layout)

# End of View

# Region: Controller
class PumpController(QMainWindow):
    """
    The Controller: Manages communication between the Model and the View.
    """
    def __init__(self):
        super().__init__()
        self.model = PumpModel()
        self.view = PumpView()
        self.initUI()
        self.last_directory = None

    def initUI(self):
        """Set up the main window and connect signals."""
        self.setWindowTitle('Pump Data Application')
        self.setCentralWidget(self.view)
        self.view.read_button.clicked.connect(self.handle_read_button_click)

    def handle_read_button_click(self):
        """
        Handle the button click: Open file dialog, load data, and update the view.
        """
        if not self.last_directory:
            self.last_directory = os.getcwd()
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Pump Data File', self.last_directory, 'Text Files (*.txt)', options=options)

        if file_path:
            self.last_directory = os.path.dirname(file_path)
            self.model.set_file_path(file_path)
            self.model.load_data()
            self.plot_results()
        else:
            self.view.result_label.setText('No file selected!')

    def plot_results(self):
        """Calculate fits and plot data."""
        coeff_head = self.model.fit_quadratic_head()
        coeff_efficiency = self.model.fit_cubic_efficiency()

        flow_rate = self.model.data['Flow Rate']
        head = self.model.data['Head']
        efficiency = self.model.data['Efficiency']

        # Generate fitted curves
        quadratic_fit = np.polyval(coeff_head, flow_rate)
        cubic_fit = np.polyval(coeff_efficiency, flow_rate)

        # Plot
        plt.figure(figsize=(10, 6))
        plt.plot(flow_rate, head, 'bo', label='Head Data')
        plt.plot(flow_rate, quadratic_fit, 'b-', label='Quadratic Fit (Head)')
        plt.plot(flow_rate, efficiency, 'ro', label='Efficiency Data')
        plt.plot(flow_rate, cubic_fit, 'r-', label='Cubic Fit (Efficiency)')
        plt.xlabel('Flow Rate (m^3/h)')
        plt.ylabel('Head (m)', color='blue')
        plt.ylabel('Efficiency (%)', color='red')
        plt.title('Pump Characteristics')
        plt.legend()
        plt.grid(True)
        plt.show()

# End of Controller

# Region: Main Application
if __name__ == '__main__':
    """
    Entry point for the application.
    """
    app = QApplication(sys.argv)
    controller = PumpController()
    controller.show()
    sys.exit(app.exec_())
# End of Main Application
