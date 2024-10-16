""" test the autoread.zmat module
"""

import numpy
import autoparse.pattern as app
import autoread


ZMA1_STR = (
    '  Geometry (in Angstrom), charge = 0, multiplicity = 1:\n'
    '\n'
    '  O\n'
    '  O       1     R1\n'
    '  H       1     R2   2     A2\n'
    '  H       2     R2   1     A2   3     D3\n'
    '\n'
    '  A2    =  96.7725720000\n'
    '  D3    = 129.3669950000\n'
    '  R1    =  1.4470582953\n'
    '  R2    =  0.9760730000\n')
ZMA2_STR = (
    'C \n'
    'O , 1 , R1 \n'
    'H , 1 , R2 , 2 , A2 \n'
    'H , 1 , R3 , 2 , A3 , 3 , D3 \n'
    'H , 1 , R4 , 2 , A4 , 3 , D4 \n'
    'H , 2 , R5 , 1 , A5 , 3 , D5 \n'
    '\n'
    'R1  = 2.67535  \n'
    'R2  = 2.06501   A2  = 109.528  \n'
    'R3  = 2.06501   A3  = 109.528   D3  = 120.808        \n'
    'R4  = 2.06458   A4  = 108.982   D4  = 240.404        \n'
    'R5  = 1.83748   A5  = 107.091   D5  = 299.596        \n')
ZMA3_STR = (
    'C \n'
    'O , 1 , R1 \n'
    'H , 1 , R2 , 2 , A2 \n'
    'H , 1 , R3 , 2 , A3 , 3 , D3 \n'
    'H , 1 , R4 , 2 , A4 , 3 , D4 \n'
    'H , 2 , R5 , 1 , A5 , 3 , D5 \n'
    '\n'
    'R1  = 4.67535  \n'
    'R2  = 4.06501   A2  = 109.528  \n'
    'R3  = 4.06501   A3  = 109.528   D3  = 120.808        \n'
    'R4  = 4.06458   A4  = 108.982   D4  = 240.404        \n'
    'R5  = 2.83748   A5  = 107.091   D5  = 299.596        \n')
ZMA4_STR = (
    'C \n')
ZMA5_STR = (
    'O \n'
    'O 1 1.454 \n'
    'H 1 0.976 2 96.77 \n'
    'H 2 0.976 1 96.77 3 129.37 \n'
)

ZMA_OUT1_STR = (
    ' comment:\n'
    ' --------\n'
    ' Symbolic Z-matrix:\n'
    ' Charge = 0 Multiplicity = 1\n'
    ' O\n'
    ' O     1 R1\n'
    ' H     1 R2  2 A2\n'
    ' H     2 R2  1 A2  3 D3  0\n'
    '  Variables:\n'
    ' R1     1.45405\n'
    '  Constants:\n'
    ' R2     0.97607\n'
    ' A2     96.77257\n'
    ' D3     129.367\n')
ZMA_OUT2_STR = (
    ' Symbolic Z-matrix:\n'
    ' Charge = 0 Multiplicity = 1\n'
    ' C\n'
    ' C     1 R1\n'
    ' H     1 R2  2 A2\n'
    ' H     1 R3  2 A3  3 D3  0\n'
    ' H     1 R4  2 A4  3 D4  0\n'
    ' C     2 R5  1 A5  3 D5  0\n'
    ' C     2 R6  1 A6  6 D6  0\n'
    ' H     6 R7  2 A7  1 D7  0\n'
    ' H     6 R8  2 A8  8 D8  0\n'
    ' H     6 R9  2 A9  8 D9  0\n'
    ' C     7 R10  2 A10  1 D10  0\n'
    ' H     7 R11  2 A11  11 D11  0\n'
    ' O     11 R12  7 A12  2 D12  0\n'
    ' H     11 R13  7 A13  13 D13  0\n'
    ' H     11 R14  7 A14  13 D14  0\n'
    ' H     13 R15  11 A15  7 D15  0\n')
ZMA_OUT3_STR = (
    ' -----------------------------------------------------------\n'
    '              Z-MATRIX (ANGSTROMS AND DEGREES)\n'
    '    nt   At 1      Lengt    2      Alph           Bet      J\n'
    ' -----------------------------------------------------------\n'
    '  1   1  C\n'
    '  2   2  O  1  1.454832( 1)\n'
    '  3   3  H  1  1.093067( 2)  2 111.219( 6)\n'
    '  4   4  H  1  1.090938( 3)  2 106.548( 7) 3 118.980( 10)  0\n'
    '  5   5  H  1  1.093052( 4)  2 111.241( 8) 3 238.017( 11)  0\n'
    '  6   6  O  2  1.360181( 5)  1 108.248( 9) 3  60.990( 12)  0\n'
    ' -----------------------------------------------------------')
ZMA_OUT4_STR = (
    ' geometry = {\n'
    ' C\n'
    ' O 1,    R1\n'
    ' H 1,    R2, 2,    A2\n'
    ' H 1,    R3, 2,    A3, 3,    D3\n'
    ' H 1,    R4, 2,    A4, 3,    D4\n'
    ' H 2,    R5, 1,    A5, 3,    D5\n'
    ' }\n')

ZMA_VAL1_STR = (
    '    A2        =   96.7725720000\n'
    '    D3        =  129.3669950000\n'
    '    R1        =    1.4470582953\n'
    '    R2        =    0.9760730000\n')
ZMA_VAL2_STR = (
    '              ----------------------------\n'
    '              !   Optimized Parameters   !\n'
    '              ! (Angstroms and Degrees)  !\n'
    ' -------------                            -----\n'
    ' !  Name     Value   Derivative information   !\n'
    ' ----------------------------------------------\n'
    ' !   R1     1.4057   -DE/DX =    0.0          !\n'
    ' !   R2     0.9761   -DE/DX =    0.0628       !\n'
    ' !   A2    96.7726   -DE/DX =    0.0552       !\n'
    ' !   D3   129.367    -DE/DX =    0.0019       !\n'
    ' ----------------------------------------------\n'
    ' GradGradGradGradGradGradGradGradGradGradGradGrad\n')
ZMA_VAL3_STR = (
    'R1  = 2.73454  \n'
    'R2  = 1.84451   A2  = 96.7726  \n'
    'R3  = 1.84451   A3  = 96.7726   D3  = 129.367        \n')
ZMA_VAL4_STR = (
    ' SETTING R1             =         1.37586100\n'
    ' SETTING R2             =         1.05835400\n'
    ' SETTING A2             =       108.86198100\n'
    ' SETTING R3             =         1.05835400\n'
    ' SETTING A3             =       108.86198100\n'
    ' SETTING D3             =       120.32113700\n'
    ' SETTING R4             =         1.05835400\n'
    ' SETTING A4             =       108.86198100\n'
    ' SETTING D4             =       234.91269600\n'
    ' SETTING R5             =         0.95251900\n'
    ' SETTING A5             =       103.13240300\n'
    ' SETTING D5             =       297.93805300\n'
    ' SETTING SPIN           =     0.00000000D+00\n'
    ' SETTING CHARGE         =     0.00000000D+00\n')
ZMA_VAL5_STR = (
    ' Optimized variables\n'
    ' R1=                  1.43218364 ANGSTROM\n'
    ' R2=                  1.09538054 ANGSTROM\n'
    ' A2=                112.03775543 DEGREE\n'
    ' R3=                  1.09538307 ANGSTROM\n'
    ' A3=                112.04463832 DEGREE\n'
    ' R4=                  1.09084803 ANGSTROM\n'
    ' A4=                108.31761858 DEGREE\n'
    ' D4=                240.16203078 DEGREE\n'
    ' D5=                299.84441753 DEGREE\n')


def test__zmat():
    """ test autoread.zmat
    """

    # Simple ZMA reads
    start_ptt = (
        app.padded(app.escape('Geometry (in Angstrom),'), app.NONNEWLINE) +
        2 * app.padded(app.NEWLINE))

    symbs, key_mat, name_mat, val_mat = autoread.zmat.read(
        ZMA1_STR,
        start_ptt=start_ptt)
    assert symbs == ('O', 'O', 'H', 'H')
    assert key_mat == ((None, None, None),
                       (1, None, None),
                       (1, 2, None),
                       (2, 1, 3))
    assert name_mat == ((None, None, None),
                        ('R1', None, None),
                        ('R2', 'A2', None),
                        ('R2', 'A2', 'D3'))
    ref_val_mat = ((None, None, None),
                   (1.4470582953, None, None),
                   (0.976073, 96.772572, None),
                   (0.976073, 96.772572, 129.36699))
    _val_mats_similar(val_mat, ref_val_mat)

    symbs, key_mat, name_mat, val_mat = autoread.zmat.read(
        ZMA2_STR,
        mat_entry_start_ptt=',',
        mat_entry_sep_ptt=',',
        setv_sep_ptt=app.padded(app.one_of_these(['', app.NEWLINE])))
    assert symbs == ('C', 'O', 'H', 'H', 'H', 'H')
    assert key_mat == ((None, None, None),
                       (1, None, None),
                       (1, 2, None),
                       (1, 2, 3),
                       (1, 2, 3),
                       (2, 1, 3))
    assert name_mat == ((None, None, None),
                        ('R1', None, None),
                        ('R2', 'A2', None),
                        ('R3', 'A3', 'D3'),
                        ('R4', 'A4', 'D4'),
                        ('R5', 'A5', 'D5'))
    ref_val_mat = ((None, None, None),
                   (2.67535, None, None),
                   (2.06501, 109.528, None),
                   (2.06501, 109.528, 120.808),
                   (2.06458, 108.982, 240.404),
                   (1.83748, 107.091, 299.596))
    _val_mats_similar(val_mat, ref_val_mat)

    symbs, key_mat, name_mat, val_mat = autoread.zmat.read(
        ZMA4_STR,
        setv_sep_ptt=app.padded(app.one_of_these(['', app.NEWLINE])))
    assert symbs == ('C',)
    assert key_mat == ((None, None, None),)
    assert name_mat == ((None, None, None),)
    assert val_mat == ((None, None, None),)

    # Check last functionality
    symbs, key_mat, name_mat, val_mat = autoread.zmat.read(
        ZMA2_STR + '\n\n' + ZMA3_STR,
        mat_entry_start_ptt=',',
        mat_entry_sep_ptt=',',
        setv_sep_ptt=app.padded(app.one_of_these(['', app.NEWLINE])),
        last=False)
    assert symbs == ('C', 'O', 'H', 'H', 'H', 'H')
    assert key_mat == ((None, None, None),
                       (1, None, None),
                       (1, 2, None),
                       (1, 2, 3),
                       (1, 2, 3),
                       (2, 1, 3))
    assert name_mat == ((None, None, None),
                        ('R1', None, None),
                        ('R2', 'A2', None),
                        ('R3', 'A3', 'D3'),
                        ('R4', 'A4', 'D4'),
                        ('R5', 'A5', 'D5'))
    ref_val_mat = ((None, None, None),
                   (2.67535, None, None),
                   (2.06501, 109.528, None),
                   (2.06501, 109.528, 120.808),
                   (2.06458, 108.982, 240.404),
                   (1.83748, 107.091, 299.596))
    _val_mats_similar(val_mat, ref_val_mat)

    # Check finding nothing (using fake start ptt not in ZMA1_STR)
    symbs, key_mat, name_mat, val_mat = autoread.zmat.read(
        ZMA1_STR, start_ptt='FAKE ZMA HEAD')
    assert symbs is None
    assert key_mat is None
    assert name_mat is None
    assert val_mat is None


def test__vmat():
    """ test autoread.zmat.matrix
    """
    start_ptt = (
        app.padded(app.NEWLINE).join([
            app.escape('Symbolic Z-matrix:'), app.LINE, '']))

    symbs, key_mat, name_mat = autoread.vmat.read(
        ZMA_OUT1_STR,
        start_ptt=start_ptt)
    assert symbs == ('O', 'O', 'H', 'H')
    assert key_mat == ((None, None, None),
                       (1, None, None),
                       (1, 2, None),
                       (2, 1, 3))
    assert name_mat == ((None, None, None),
                        ('R1', None, None),
                        ('R2', 'A2', None),
                        ('R2', 'A2', 'D3'))

    start_ptt = (
        app.padded(app.NEWLINE).join([
            app.escape('Symbolic Z-matrix:'), app.LINE, '']))

    symbs, key_mat, name_mat = autoread.vmat.read(
        ZMA_OUT2_STR,
        start_ptt=start_ptt,
        line_end_ptt=app.maybe(app.UNSIGNED_INTEGER))
    assert symbs == (
        'C', 'C', 'H', 'H', 'H', 'C', 'C', 'H', 'H', 'H', 'C', 'H', 'O', 'H',
        'H', 'H')
    assert key_mat == (
        (None, None, None),
        (1, None, None),
        (1, 2, None),
        (1, 2, 3),
        (1, 2, 3),
        (2, 1, 3),
        (2, 1, 6),
        (6, 2, 1),
        (6, 2, 8),
        (6, 2, 8),
        (7, 2, 1),
        (7, 2, 11),
        (11, 7, 2),
        (11, 7, 13),
        (11, 7, 13),
        (13, 11, 7))
    assert name_mat == (
        (None, None, None),
        ('R1', None, None),
        ('R2', 'A2', None),
        ('R3', 'A3', 'D3'),
        ('R4', 'A4', 'D4'),
        ('R5', 'A5', 'D5'),
        ('R6', 'A6', 'D6'),
        ('R7', 'A7', 'D7'),
        ('R8', 'A8', 'D8'),
        ('R9', 'A9', 'D9'),
        ('R10', 'A10', 'D10'),
        ('R11', 'A11', 'D11'),
        ('R12', 'A12', 'D12'),
        ('R13', 'A13', 'D13'),
        ('R14', 'A14', 'D14'),
        ('R15', 'A15', 'D15'))

    line_start_ptt = app.LINESPACES.join(2 * [app.UNSIGNED_INTEGER])
    entry_end_ptt = app.PADDING.join([
        app.escape('('), app.UNSIGNED_INTEGER, app.escape(')'),
        app.maybe(app.UNSIGNED_INTEGER)])
    start_ptt = (
        app.padded(app.NEWLINE).join([
            app.escape('Z-MATRIX (ANGSTROMS AND DEGREES)'),
            app.LINE, app.LINE, '']))

    symbs, key_mat, name_mat = autoread.vmat.read(
        ZMA_OUT3_STR,
        start_ptt=start_ptt,
        name_ptt=app.FLOAT,
        line_start_ptt=line_start_ptt,
        entry_end_ptt=entry_end_ptt)
    assert symbs == ('C', 'O', 'H', 'H', 'H', 'O')
    assert key_mat == ((None, None, None),
                       (1, None, None),
                       (1, 2, None),
                       (1, 2, 3),
                       (1, 2, 3),
                       (2, 1, 3))
    assert name_mat == ((None, None, None),
                        (1.454832, None, None),
                        (1.093067, 111.219, None),
                        (1.090938, 106.548, 118.98),
                        (1.093052, 111.241, 238.017),
                        (1.360181, 108.248, 60.99))

    start_ptt = (
        app.maybe(app.SPACES).join([
            'geometry', app.escape('='), app.escape('{'), '']))

    symbs, key_mat, name_mat = autoread.vmat.read(
        ZMA_OUT4_STR,
        start_ptt=start_ptt,
        entry_start_ptt=app.maybe(','),
        entry_sep_ptt=',')
    assert symbs == ('C', 'O', 'H', 'H', 'H', 'H')
    assert key_mat == ((None, None, None),
                       (1, None, None),
                       (1, 2, None),
                       (1, 2, 3),
                       (1, 2, 3),
                       (2, 1, 3))
    assert name_mat == ((None, None, None),
                        ('R1', None, None),
                        ('R2', 'A2', None),
                        ('R3', 'A3', 'D3'),
                        ('R4', 'A4', 'D4'),
                        ('R5', 'A5', 'D5'))

    symbs, key_mat, name_mat = autoread.vmat.read(
        ZMA5_STR,
        name_ptt=app.FLOAT)
    assert symbs == ('O', 'O', 'H', 'H')
    assert key_mat == ((None, None, None),
                       (1, None, None),
                       (1, 2, None),
                       (2, 1, 3))
    ref_name_mat = (
        (None, None, None),
        (1.454, None, None),
        (0.976, 96.77, None),
        (0.976, 96.77, 129.37))
    _val_mats_similar(name_mat, ref_name_mat)

    # Check grabbing first zma (ZMA5 here)
    symbs, key_mat, name_mat = autoread.vmat.read(
        ZMA5_STR + '\n\n\n' + ZMA3_STR + '\n\n\n' + ZMA1_STR,
        name_ptt=app.FLOAT,
        last=False)
    assert symbs == ('O', 'O', 'H', 'H')
    assert key_mat == ((None, None, None),
                       (1, None, None),
                       (1, 2, None),
                       (2, 1, 3))
    ref_name_mat = (
        (None, None, None),
        (1.454, None, None),
        (0.976, 96.77, None),
        (0.976, 96.77, 129.37))
    _val_mats_similar(name_mat, ref_name_mat)

    # Check grabbing nothing
    symbs, key_mat, name_mat = autoread.vmat.read(
        '', name_ptt=app.FLOAT)
    assert symbs is None
    assert key_mat is None
    assert name_mat is None

    # symbs, key_mat, name_mat = autoread.vmat.read(
    #     ZMA5_STR, name_ptt=app.LETTER)
    # print(key_mat)
    # print(name_mat)
    # assert symbs is None
    # assert key_mat is None
    # assert name_mat is None


def test__setval():
    """ test autoread.zmat.setval
    """

    val_dct = autoread.setval.read(ZMA_VAL1_STR)
    assert val_dct == {
        'A2': 96.772572, 'D3': 129.366995, 'R1': 1.4470582953, 'R2': 0.976073}

    start_ptt = app.padded(app.NEWLINE).join([
        app.escape('!   Optimized Parameters   !'),
        app.LINE, app.LINE, app.LINE, app.LINE, ''])

    val_dct = autoread.setval.read(
        ZMA_VAL2_STR,
        start_ptt=start_ptt,
        entry_sep_ptt='',
        entry_start_ptt=app.escape('!'),
        sep_ptt=app.maybe(app.LINESPACES).join([
            app.escape('-DE/DX ='), app.FLOAT, app.escape('!'), app.NEWLINE]))
    assert val_dct == {
        'R1': 1.4057, 'R2': 0.9761, 'A2': 96.7726, 'D3': 129.367}

    val_dct = autoread.setval.read(
        ZMA_VAL3_STR,
        sep_ptt=app.one_of_these(['', app.NEWLINE]))
    assert val_dct == {
        'R1': 2.73454, 'R2': 1.84451, 'A2': 96.7726, 'R3': 1.84451,
        'A3': 96.7726, 'D3': 129.367}

    val_dct = autoread.setval.read(
        ZMA_VAL4_STR,
        entry_start_ptt='SETTING',
        val_ptt=app.one_of_these([app.EXPONENTIAL_FLOAT_D, app.NUMBER]),
        last=False,
        case=False)
    assert val_dct == {
        'R1': 1.375861, 'R2': 1.058354, 'A2': 108.861981, 'R3': 1.058354,
        'A3': 108.861981, 'D3': 120.321137, 'R4': 1.058354, 'A4': 108.861981,
        'D4': 234.912696, 'R5': 0.952519, 'A5': 103.132403, 'D5': 297.938053,
        'SPIN': 0.0, 'CHARGE': 0.0}

    val_dct = autoread.setval.read(
        ZMA_VAL5_STR,
        start_ptt=app.padded('Optimized variables') + app.NEWLINE,
        entry_end_ptt=app.one_of_these(['ANGSTROM', 'DEGREE']),
        last=True,
        case=False)
    assert val_dct == {
        'R1': 1.43218364, 'R2': 1.09538054, 'A2': 112.03775543,
        'R3': 1.09538307, 'A3': 112.04463832, 'R4': 1.09084803,
        'A4': 108.31761858, 'D4': 240.16203078, 'D5': 299.84441753}


# Helper
def _val_mats_similar(val_mat, ref_val_mat):
    """ Check if two value matrices are the same
    """
    for i, row in enumerate(val_mat):
        for j, val in enumerate(row):
            ref_val = ref_val_mat[i][j]
            if val is None:
                assert ref_val is None
            else:
                assert numpy.isclose(val, ref_val)
