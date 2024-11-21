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

from pymeasure.test import expected_protocol
from pymeasure.instruments.siglenttechnologies import SDM3045X


def test_init():
    with expected_protocol(
        SDM3045X,
        [
            (b"*CLS", None),
            (b"*RST", None),
            (b"SYSTem:ERRor?", b'0,"No error"\n')
        ],
    ):
        pass  # Verify the expected communication on initialization


def test_get_id():
    with expected_protocol(
        SDM3045X,
        [(b"*IDN?", b"Siglent Technologies,SDM3045X,SN123456,V1.0.0\n")],
    ) as inst:
        idn = inst.get_id()
        assert idn == "Siglent Technologies,SDM3045X,SN123456,V1.0.0"


def test_voltage_dc_measurement():
    with expected_protocol(
        SDM3045X,
        [
            (b"CONFigure:VOLTage:DC 10", None),
            (b"MEASure:VOLTage:DC?", b"5.123\n"),
            (b"SYSTem:ERRor?", b'0,"No error"\n')
        ],
    ) as inst:
        inst.configure_voltage_dc(voltage_range=10)
        voltage = inst.voltage_dc
        assert voltage == 5.123


def test_current_dc_measurement():
    with expected_protocol(
        SDM3045X,
        [
            (b"CONFigure:CURRent:DC 1", None),
            (b"MEASure:CURRent:DC?", b"0.0123\n"),
            (b"SYSTem:ERRor?", b'0,"No error"\n')
        ],
    ) as inst:
        inst.configure_current_dc(current_range=1)
        current = inst.current_dc
        assert current == 0.0123


def test_resistance_measurement():
    with expected_protocol(
        SDM3045X,
        [
            (b"SENSe:RESistance:MODE RESistance", None),
            (b"CONFigure:RESistance 1000", None),
            (b"MEASure:RESistance?", b"123.45\n"),
            (b"SYSTem:ERRor?", b'0,"No error"\n')
        ],
    ) as inst:
        inst.configure_resistance(resistance_range=1000)
        resistance = inst.resistance
        assert resistance == 123.45


def test_temperature_measurement():
    with expected_protocol(
        SDM3045X,
        [
            (b"TEMPerature:TRANsducer TC", None),
            (b"TEMPerature:TC:TYPE K", None),
            (b"TEMPerature:TC:RJUNction INT", None),
            (b"MEASure:TEMPerature?", b"25.0\n"),
            (b"SYSTem:ERRor?", b'0,"No error"\n')
        ],
    ) as inst:
        inst.configure_temperature(
            transducer_type='TC',
            transducer_settings={
                'TYPE': 'K',
                'REFERENCE': 'INT'
            }
        )
        temperature = inst.temperature
        assert temperature == 25.0


def test_trigger():
    with expected_protocol(
        SDM3045X,
        [
            (b"TRIGger:SOURce BUS", None),
            (b"INITiate", None),
            (b"FETCh?", b"3.1416\n"),
            (b"SYSTem:ERRor?", b'0,"No error"\n')
        ],
    ) as inst:
        inst.trigger_source = 'BUS'
        inst.trigger()
        result = inst.fetch()
        assert result == 3.1416


def test_error_handling():
    with expected_protocol(
        SDM3045X,
        [
            (b"*RST", None),
            (b"SYSTem:ERRor?", b'-200,"Execution error"\n')
        ],
    ) as inst:
        try:
            inst.reset()
        except Exception as e:
            assert str(e) == 'Instrument Error -200: Execution error'
