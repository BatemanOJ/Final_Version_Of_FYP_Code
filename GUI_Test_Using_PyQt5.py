import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSlider,
    QPushButton,
    QCheckBox,
)
from PyQt5.QtCore import Qt, QTimer

class EngineeringTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Engineering Tool")
        self.setGeometry(100, 100, 750, 700)

        # Default values nissan
        self.input_range = 170
        self.input_energy = 28000
        self.input_discharging_power = 90000
        self.input_max_V = 400
        self.input_min_V = 240
        self.input_max_mass_pack = 315
        self.input_charging_power = 50000

        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Label
        self.label = QLabel("Please enter desired EV characteristics values or adjust slider:")
        self.layout.addWidget(self.label)

        # Range
        self.range_entry = QLineEdit(self)
        self.range_entry.setPlaceholderText("Range")
        self.range_slider = QSlider(Qt.Horizontal)
        self.range_slider.setRange(0, 1000)
        self.range_slider.setValue(self.input_range)
        self.range_label = QLabel(str(self.input_range))
        self.add_row("Range", self.range_entry, self.range_slider, self.range_label)

        # Total Energy
        self.total_energy_entry = QLineEdit(self)
        self.total_energy_entry.setPlaceholderText("Total Energy")
        self.total_energy_slider = QSlider(Qt.Horizontal)
        self.total_energy_slider.setRange(0, 150000)
        self.total_energy_slider.setValue(self.input_energy)
        self.total_energy_label = QLabel(str(self.input_energy))
        self.add_row("Total Energy", self.total_energy_entry, self.total_energy_slider, self.total_energy_label)

        # Pack Mass
        self.pack_mass_entry = QLineEdit(self)
        self.pack_mass_entry.setPlaceholderText("Pack Mass")
        self.pack_mass_slider = QSlider(Qt.Horizontal)
        self.pack_mass_slider.setRange(0, 1000)
        self.pack_mass_slider.setValue(self.input_max_mass_pack)
        self.pack_mass_label = QLabel(str(self.input_max_mass_pack))
        self.add_row("Pack Mass", self.pack_mass_entry, self.pack_mass_slider, self.pack_mass_label)

        # Max Voltage
        self.max_V_entry = QLineEdit(self)
        self.max_V_entry.setPlaceholderText("Maximum Voltage")
        self.max_V_slider = QSlider(Qt.Horizontal)
        self.max_V_slider.setRange(0, 1000)
        self.max_V_slider.setValue(self.input_max_V)
        self.max_V_label = QLabel(str(self.input_max_V))
        self.add_row("Max Voltage", self.max_V_entry, self.max_V_slider, self.max_V_label)

        # Min Voltage
        self.min_V_entry = QLineEdit(self)
        self.min_V_entry.setPlaceholderText("Minimum Voltage")
        self.min_V_slider = QSlider(Qt.Horizontal)
        self.min_V_slider.setRange(0, 600)
        self.min_V_slider.setValue(self.input_min_V)
        self.min_V_label = QLabel(str(self.input_min_V))
        self.add_row("Min Voltage", self.min_V_entry, self.min_V_slider, self.min_V_label)

        # Discharging Power
        self.discharging_power_entry = QLineEdit(self)
        self.discharging_power_entry.setPlaceholderText("Peak Discharging Power")
        self.discharging_power_slider = QSlider(Qt.Horizontal)
        self.discharging_power_slider.setRange(0, 500000)
        self.discharging_power_slider.setValue(self.input_discharging_power)
        self.discharging_power_label = QLabel(str(self.input_discharging_power))
        self.add_row("Discharging Power", self.discharging_power_entry, self.discharging_power_slider, self.discharging_power_label)

        # Charging Power
        self.charging_power_entry = QLineEdit(self)
        self.charging_power_entry.setPlaceholderText("Peak Charging Power")
        self.charging_power_slider = QSlider(Qt.Horizontal)
        self.charging_power_slider.setRange(0, 300000)
        self.charging_power_slider.setValue(self.input_charging_power)
        self.charging_power_label = QLabel(str(self.input_charging_power))
        self.add_row("Charging Power", self.charging_power_entry, self.charging_power_slider, self.charging_power_label)

        # Calculate Button
        self.calc_button = QPushButton("Calculate", self)
        self.calc_button.clicked.connect(self.calculate)
        self.layout.addWidget(self.calc_button)

        # Result Label
        self.result_label = QLabel("Result: ")
        self.layout.addWidget(self.result_label)

        # Checkbox for transferring values to sliders
        self.checkbox = QCheckBox("Transfer numbers entered to sliders?", self)
        self.checkbox.setChecked(True)
        self.layout.addWidget(self.checkbox)

        # Connect signals
        self.connect_signals()

    def add_row(self, label_text, entry, slider, value_label):
        row_layout = QHBoxLayout()
        row_layout.addWidget(QLabel(label_text))
        row_layout.addWidget(entry)
        row_layout.addWidget(slider)
        row_layout.addWidget(value_label)
        self.layout.addLayout(row_layout)

    def connect_signals(self):
        # Connect sliders to update labels
        self.range_slider.valueChanged.connect(lambda: self.update_label(self.range_label, self.range_slider.value()))
        self.total_energy_slider.valueChanged.connect(lambda: self.update_label(self.total_energy_label, self.total_energy_slider.value()))
        self.pack_mass_slider.valueChanged.connect(lambda: self.update_label(self.pack_mass_label, self.pack_mass_slider.value()))
        self.max_V_slider.valueChanged.connect(lambda: self.update_label(self.max_V_label, self.max_V_slider.value()))
        self.min_V_slider.valueChanged.connect(lambda: self.update_label(self.min_V_label, self.min_V_slider.value()))
        self.discharging_power_slider.valueChanged.connect(lambda: self.update_label(self.discharging_power_label, self.discharging_power_slider.value()))
        self.charging_power_slider.valueChanged.connect(lambda: self.update_label(self.charging_power_label, self.charging_power_slider.value()))

        # Connect entries to update sliders
        self.range_entry.textChanged.connect(self.update_sliders)
        self.total_energy_entry.textChanged.connect(self.update_sliders)
        self.pack_mass_entry.textChanged.connect(self.update_sliders)
        self.max_V_entry.textChanged.connect(self.update_sliders)
        self.min_V_entry.textChanged.connect(self.update_sliders)
        self.discharging_power_entry.textChanged.connect(self.update_sliders)
        self.charging_power_entry.textChanged.connect(self.update_sliders)

    def update_label(self, label, value):
        label.setText(str(value))

    def update_sliders(self):
        if self.checkbox.isChecked():
            self.update_slider_from_entry(self.range_entry, self.range_slider)
            self.update_slider_from_entry(self.total_energy_entry, self.total_energy_slider)
            self.update_slider_from_entry(self.pack_mass_entry, self.pack_mass_slider)
            self.update_slider_from_entry(self.max_V_entry, self.max_V_slider)
            self.update_slider_from_entry(self.min_V_entry, self.min_V_slider)
            self.update_slider_from_entry(self.discharging_power_entry, self.discharging_power_slider)
            self.update_slider_from_entry(self.charging_power_entry, self.charging_power_slider)

    def update_slider_from_entry(self, entry, slider):
        try:
            value = float(entry.text())
            if slider.minimum() <= value <= slider.maximum():
                slider.setValue(int(value))
        except ValueError:
            pass

    def calculate(self):
        # Get values from entries or sliders
        req_range = self.get_value(self.range_entry, self.range_slider)
        req_energy = self.get_value(self.total_energy_entry, self.total_energy_slider)
        req_max_mass_pack = self.get_value(self.pack_mass_entry, self.pack_mass_slider)
        req_max_V = self.get_value(self.max_V_entry, self.max_V_slider)
        req_min_V = self.get_value(self.min_V_entry, self.min_V_slider)
        req_discharging_power = self.get_value(self.discharging_power_entry, self.discharging_power_slider)
        req_charging_power = self.get_value(self.charging_power_entry, self.charging_power_slider)

        # Display result (placeholder for actual calculation)
        self.result_label.setText(
            f"Range: {req_range}\n"
            f"Total Energy: {req_energy}\n"
            f"Pack Mass: {req_max_mass_pack}\n"
            f"Max Voltage: {req_max_V}\n"
            f"Min Voltage: {req_min_V}\n"
            f"Discharging Power: {req_discharging_power}\n"
            f"Charging Power: {req_charging_power}"
        )

    def get_value(self, entry, slider):
        try:
            return float(entry.text())
        except ValueError:
            return slider.value()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EngineeringTool()
    window.show()
    sys.exit(app.exec_())