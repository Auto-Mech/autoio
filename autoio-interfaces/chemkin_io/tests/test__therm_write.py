""" Tests the writer functions in mechanism.py pertaining to thermo
"""

import difflib
from chemkin_io.writer import mechanism

SPC_NASA7_DCT = {
    'O2': ['RUS 89', 'O   2               ', 'G', [200.0, 6000.0, 1000.0],
           ([2.54363697E+00, -2.73162486E-05, -4.19029520E-09, 4.95481845E-12,
             -4.79553694E-16, 2.92260120E+04, 4.92229457E+00],
            [3.16826710E+00, -3.27931884E-03, 6.64306396E-06, -6.12806624E-09,
             2.11265971E-12, 2.91222592E+04, 2.05193346E+00])
           ],
    'N2O': ['L 7/88', 'N   1O   1          ', 'G', [200.0, 6000.0, 1000.0],
            ([0.48230729E+01, 0.26270251E-02, -0.95850872E-06, 0.16000712E-09,
              -0.97752302E-14, 0.80734047E+04, -0.22017208E+01],
             [0.22571502E+01, 0.11304728E-01, -0.13671319E-04, 0.96819803E-08,
              -0.29307182E-11, 0.87417746E+04, 0.10757992E+02])
            ]
}

THERM_STR = (
    'THERMO\n'
    '200.00    1000.00   5000.000\n\n'
    'O2                RUS 89O   2               G    200.00   6000.00 1000.00      1\n'
    ' 2.54363697E+00-2.73162486E-05-4.19029520E-09 4.95481845E-12-4.79553694E-16    2\n'
    ' 2.92260120E+04 4.92229457E+00 3.16826710E+00-3.27931884E-03 6.64306396E-06    3\n'
    '-6.12806624E-09 2.11265971E-12 2.91222592E+04 2.05193346E+00                   4\n'
    'N2O               L 7/88N   1O   1          G    200.00   6000.00 1000.00      1\n'
    ' 4.82307290E+00 2.62702510E-03-9.58508720E-07 1.60007120E-10-9.77523020E-15    2\n'
    ' 8.07340470E+03-2.20172080E+00 2.25715020E+00 1.13047280E-02-1.36713190E-05    3\n'
    ' 9.68198030E-09-2.93071820E-12 8.74177460E+03 1.07579920E+01                   4\n\n'
    'END\n\n\n'
)


def test_therm():
    """ Tests the thermo block writer
    """
    out_str = mechanism.write_chemkin_file(spc_nasa7_dct=SPC_NASA7_DCT)
    assert out_str == THERM_STR


if __name__ == '__main__':
    test_therm()
