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
        'FREQ', 'PER', 'DIOD', 'CONT', 'CAP', 'TEMP'.""",
        validator=strict_discrete_set,
        values=[
            'VOLT:DC', 'VOLT:AC',
            'CURR:DC', 'CURR:AC',
            'RES', 'FREQ', 'PER', 'DIOD', 'CONT',
            'CAP', 'TEMP'
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

    # Capacitance range property
    capacitance_range = Instrument.control(
        "CAPacitance:RANGe?", "CAPacitance:RANGe %g",
        """A floating point property that sets the capacitance measurement range in farads.
        Acceptable values depend on the function selected.""",
        validator=strict_range,
        values=[1e-9, 1],  # Adjust ranges based on instrument specifications
    )

    # Temperature type property
    temperature_transducer = Instrument.control(
        "TEMPerature:TRANsducer?", "TEMPerature:TRANsducer %s",
        """A string property that sets the temperature transducer type.
        Valid values are 'RTD', 'THER', 'TC'.""",
        validator=strict_discrete_set,
        values=['RTD', 'THER', 'TC'],
    )

    # Thermocouple type property
    thermocouple_type = Instrument.control(
        "TEMPerature:TC:TYPE?", "TEMPerature:TC:TYPE %s",
        """A string property that sets the thermocouple type.
        Valid values are 'B', 'E', 'J', 'K', 'N', 'R', 'S', 'T'.""",
        validator=strict_discrete_set,
        values=['B', 'E', 'J', 'K', 'N', 'R', 'S', 'T'],
    )

    # RTD type property
    rtd_type = Instrument.control(
        "TEMPerature:RTD:TYPE?", "TEMPerature:RTD:TYPE %s",
        """A string property that sets the RTD type.
        Valid values are 'PT100', 'PT385', 'PT392', 'PT3916'.""",
        validator=strict_discrete_set,
        values=['PT100', 'PT385', 'PT392', 'PT3916'],
    )

    # Thermistor type property
    thermistor_type = Instrument.control(
        "TEMPerature:THERmistor:TYPE?", "TEMPerature:THERmistor:TYPE %s",
        """A string property that sets the thermistor type.
        Valid values are '2252', '5K', '10K', '20K', '50K', '100K'.""",
        validator=strict_discrete_set,
        values=['2252', '5K', '10K', '20K', '50K', '100K'],
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

    # Capacitance measurement
    capacitance = Instrument.measurement(
        "MEASure:CAPacitance?",
        """Measures and returns the capacitance in farads."""
    )

    # Temperature measurement
    temperature = Instrument.measurement(
        "MEASure:TEMPerature?",
        """Measures and returns the temperature in degrees Celsius."""
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
        """Performs a continuity test and returns True if continuity is detected.""",
        get_process=lambda v: bool(int(v.strip()))
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
            error_response = self.ask("SYSTem:ERRor?")
            error_response = error_response.strip()
            if not error_response:
                # Empty response, assume no errors
                break

            # Attempt to parse the error response
            if ',' in error_response:
                error_code_str, error_message = error_response.split(',', 1)
                error_message = error_message.strip().strip('"')
            else:
                error_code_str = error_response
                error_message = 'No error message'

            try:
                error_code = int(error_code_str)
            except ValueError:
                # Handle non-integer error codes
                error_code = -1  # Assign a generic error code
                error_message = error_response

            if error_code == 0:
                # No error
                break
            else:
                raise Exception(f"Instrument Error {error_code}: {error_message}")

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

    def configure_resistance(self, resistance_range=None, four_wire=False):
        """
        Configures the instrument for resistance measurement.

        :param resistance_range: The measurement range in ohms (float).
        :param four_wire: Set to True for 4-wire measurement.
        """
        if four_wire:
            self.write("SENSe:RESistance:MODE FRESistance")
        else:
            self.write("SENSe:RESistance:MODE RESistance")
        cmd = "CONFigure:RESistance"
        if resistance_range is not None:
            cmd += f" {resistance_range}"
        self.write(cmd)
        self.check_errors()

    def configure_capacitance(self, capacitance_range=None):
        """
        Configures the instrument for capacitance measurement.

        :param capacitance_range: The measurement range in farads (float).
        """
        cmd = "CONFigure:CAPacitance"
        if capacitance_range is not None:
            cmd += f" {capacitance_range}"
        self.write(cmd)
        self.check_errors()

    def configure_temperature(self, transducer_type='RTD', transducer_settings=None):
        """
        Configures the instrument for temperature measurement.

        :param transducer_type: The transducer type ('RTD', 'THER', 'TC').
        :param transducer_settings: Dictionary with settings specific to the transducer type.
        """
        transducer_type = transducer_type.upper()
        valid_types = ['RTD', 'THER', 'TC']
        if transducer_type not in valid_types:
            raise ValueError(f"Invalid transducer type '{transducer_type}'. Valid options are {valid_types}")
        self.write(f"TEMPerature:TRANsducer {transducer_type}")
        self.check_errors()

        if transducer_settings:
            if transducer_type == 'RTD':
                rtd_type = transducer_settings.get('TYPE', 'PT100')
                self.write(f"TEMPerature:RTD:TYPE {rtd_type}")
                self.check_errors()
                # Set RTD connection mode (2-wire, 3-wire, 4-wire)
                connection = transducer_settings.get('CONNECTION', '4')
                self.write(f"TEMPerature:RTD:CONNection {connection}")
                self.check_errors()
            elif transducer_type == 'THER':
                ther_type = transducer_settings.get('TYPE', '10K')
                self.write(f"TEMPerature:THERmistor:TYPE {ther_type}")
                self.check_errors()
            elif transducer_type == 'TC':
                tc_type = transducer_settings.get('TYPE', 'K')
                self.write(f"TEMPerature:TC:TYPE {tc_type}")
                self.check_errors()
                # Set reference junction (internal, external)
                reference = transducer_settings.get('REFERENCE', 'INT')
                self.write(f"TEMPerature:TC:RJUNction {reference}")
                self.check_errors()

    def configure_frequency(self, voltage_range=None):
        """
        Configures the instrument for frequency measurement.

        :param voltage_range: The voltage range in volts (float).
        """
        cmd = "CONFigure:FREQuency"
        if voltage_range is not None:
            cmd += f" {voltage_range}"
        self.write(cmd)
        self.check_errors()

    def configure_period(self, voltage_range=None):
        """
        Configures the instrument for period measurement.

        :param voltage_range: The voltage range in volts (float).
        """
        cmd = "CONFigure:PERiod"
        if voltage_range is not None:
            cmd += f" {voltage_range}"
        self.write(cmd)
        self.check_errors()

    def configure_diode(self):
        """
        Configures the instrument for diode test measurement.
        """
        self.write("CONFigure:DIODe")
        self.check_errors()

    def configure_continuity(self):
        """
        Configures the instrument for continuity test measurement.
        """
        self.write("CONFigure:CONTinuity")
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
