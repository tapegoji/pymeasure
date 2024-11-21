#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2024 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import strict_discrete_set, strict_range

class SDM3045X(Instrument):
    """
    Represents the Siglent Technologies SDM3045X Digital Multimeter.

    Provides methods and properties to interact with the instrument via SCPI commands.

    Example usage:

    ```python
    from pymeasure.instruments.siglenttechnologies import SDM3045X

    dmm = SDM3045X("TCPIP0::10.11.1.3.220::INSTR")
    voltage = dmm.voltage_dc
    print(f"Measured Voltage: {voltage} V")
    ```
    """

    ######################################################################
    # Instrument control and measurement functions
    ######################################################################

    # Measurement function property
    function = Instrument.control(
        "FUNCtion?", "FUNCtion %s",
        """A string property that sets the measurement function of the instrument.
        Valid values are 'VOLT:DC', 'VOLT:AC', 'CURR:DC', 'CURR:AC', 'RES',
        'FREQ', 'PER', 'DIOD', 'CONT'.""",
        validator=strict_discrete_set,
        values=[
            'VOLT:DC', 'VOLT:AC',
            'CURR:DC', 'CURR:AC',
            'RES', 'FREQ', 'PER', 'DIOD', 'CONT'
        ],
        get_process=lambda v: v.strip('"'),
        set_process=lambda v: f'"{v}"'
    )

    # Voltage range property
    voltage_range = Instrument.control(
        "VOLTage:RANGe?", "VOLTage:RANGe %g",
        """A floating point property that sets the voltage measurement range in volts.
        Acceptable values depend on the function selected.""",
        validator=strict_range,
        values=[0.1, 1000],  # Adjust ranges based on instrument specifications
    )

    # Current range property
    current_range = Instrument.control(
        "CURRent:RANGe?", "CURRent:RANGe %g",
        """A floating point property that sets the current measurement range in amperes.
        Acceptable values depend on the function selected.""",
        validator=strict_range,
        values=[0.00001, 10],  # Adjust ranges based on instrument specifications
    )

    # Resistance range property
    resistance_range = Instrument.control(
        "RESistance:RANGe?", "RESistance:RANGe %g",
        """A floating point property that sets the resistance measurement range in ohms.
        Acceptable values depend on the function selected.""",
        validator=strict_range,
        values=[0.1, 100000000],  # Adjust ranges based on instrument specifications
    )

    # Trigger source property
    trigger_source = Instrument.control(
        "TRIGger:SOURce?", "TRIGger:SOURce %s",
        """A string property that sets the trigger source.
        Valid values are 'IMM', 'EXT', 'BUS'.""",
        validator=strict_discrete_set,
        values=['IMM', 'EXT', 'BUS'],
    )

    # DC Voltage measurement
    voltage_dc = Instrument.measurement(
        "MEASure:VOLTage:DC?",
        """Measures and returns the DC voltage in volts."""
    )

    # AC Voltage measurement
    voltage_ac = Instrument.measurement(
        "MEASure:VOLTage:AC?",
        """Measures and returns the AC voltage in volts."""
    )

    # DC Current measurement
    current_dc = Instrument.measurement(
        "MEASure:CURRent:DC?",
        """Measures and returns the DC current in amperes."""
    )

    # AC Current measurement
    current_ac = Instrument.measurement(
        "MEASure:CURRent:AC?",
        """Measures and returns the AC current in amperes."""
    )

    # Resistance measurement
    resistance = Instrument.measurement(
        "MEASure:RESistance?",
        """Measures and returns the resistance in ohms."""
    )

    # Frequency measurement
    frequency = Instrument.measurement(
        "MEASure:FREQuency?",
        """Measures and returns the frequency in hertz."""
    )

    # Period measurement
    period = Instrument.measurement(
        "MEASure:PERiod?",
        """Measures and returns the period in seconds."""
    )

    # Diode test measurement
    diode_voltage = Instrument.measurement(
        "MEASure:DIODe?",
        """Measures and returns the voltage drop across a diode in volts."""
    )

    # Continuity test measurement
    continuity = Instrument.measurement(
        "MEASure:CONTinuity?",
        """Performs a continuity test and returns True if continuity is detected."""
    )

    ######################################################################
    # Initialization and utility methods
    ######################################################################

    def __init__(self, resourceName, **kwargs):
        super().__init__(
            resourceName,
            "Siglent SDM3045X Digital Multimeter",
            includeSCPI=True,
            read_termination='\n',
            write_termination='\n',
            timeout=10000,  # Adjust timeout as needed
            **kwargs
        )
        self.clear_status()
        self.reset()
        self.check_errors()

    def reset(self):
        """Resets the instrument to its default settings."""
        self.write("*RST")
        self.check_errors()

    def clear_status(self):
        """Clears the instrument's status registers and error queue."""
        self.write("*CLS")

    def check_errors(self):
        """
        Checks for instrument errors and raises an exception if any are found.
        """
        while True:
            error = self.ask("SYSTem:ERRor?")
            error_code, error_message = error.strip().split(',', 1)
            error_code = int(error_code)
            if error_code == 0:
                break
            else:
                raise Exception(f"Instrument Error {error_code}: {error_message.strip('\"')}")

    ######################################################################
    # Configuration methods
    ######################################################################

    def configure_voltage_dc(self, voltage_range=None):
        """
        Configures the instrument for DC voltage measurement.

        :param voltage_range: The measurement range in volts (float).
        """
        cmd = "CONFigure:VOLTage:DC"
        if voltage_range is not None:
            cmd += f" {voltage_range}"
        self.write(cmd)
        self.check_errors()

    def configure_voltage_ac(self, voltage_range=None):
        """
        Configures the instrument for AC voltage measurement.

        :param voltage_range: The measurement range in volts (float).
        """
        cmd = "CONFigure:VOLTage:AC"
        if voltage_range is not None:
            cmd += f" {voltage_range}"
        self.write(cmd)
        self.check_errors()

    def configure_current_dc(self, current_range=None):
        """
        Configures the instrument for DC current measurement.

        :param current_range: The measurement range in amperes (float).
        """
        cmd = "CONFigure:CURRent:DC"
        if current_range is not None:
            cmd += f" {current_range}"
        self.write(cmd)
        self.check_errors()

    def configure_current_ac(self, current_range=None):
        """
        Configures the instrument for AC current measurement.

        :param current_range: The measurement range in amperes (float).
        """
        cmd = "CONFigure:CURRent:AC"
        if current_range is not None:
            cmd += f" {current_range}"
        self.write(cmd)
        self.check_errors()

    def configure_resistance(self, resistance_range=None):
        """
        Configures the instrument for resistance measurement.

        :param resistance_range: The measurement range in ohms (float).
        """
        cmd = "CONFigure:RESistance"
        if resistance_range is not None:
            cmd += f" {resistance_range}"
        self.write(cmd)
        self.check_errors()

    ######################################################################
    # Trigger methods
    ######################################################################

    def trigger(self):
        """
        Sends a trigger signal to the instrument to initiate a measurement.
        """
        self.write("INITiate")
        self.check_errors()

    def fetch(self):
        """
        Fetches the last measurement result.

        :returns: The measured value as a float.
        """
        result = self.ask("FETCh?")
        self.check_errors()
        return float(result)

    ######################################################################
    # Additional methods
    ######################################################################

    def get_id(self):
        """
        Queries the instrument identification string.

        :returns: The identification string.
        """
        idn = self.ask("*IDN?")
        return idn.strip()

    def self_test(self):
        """
        Runs the instrument self-test.

        :returns: True if the self-test passes, False otherwise.
        """
        result = int(self.ask("*TST?"))
        self.check_errors()
        return result == 0

    def measure(self):
        """
        Performs a measurement based on the current function setting.

        :returns: The measured value as a float.
        """
        result = self.ask("READ?")
        self.check_errors()
        return float(result)
