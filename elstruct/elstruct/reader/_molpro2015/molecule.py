""" molecular geometry and structure readers
"""
import numpy
import autoread as ar
import autoparse.pattern as app
import automol


MOLPRO_ENTRY_START_PATTERN = (
        'SETTING' + app.SPACES +
        app.one_of_these(['R', 'A', 'D']) +
        app.one_or_more(app.INTEGER)
)
# 'SETTING' + app.not_followed_by(app.padded('MOLPRO_ENERGY')),
# 'SETTING' + app.not_followed_by('MOLPRO_ENERGY'),
# 'SETTING' + app.not_followed_by(app.padded('SPIN')),
# 'SETTING' + app.not_followed_by(app.padded('CHARGE'))


def opt_geometry(output_str):
    """ Reads the optimized molecular geometry (in Cartesian coordinates) from
        the output file string. Returns the geometry in Bohr.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: automol molecular geometry data structure
    """

    ptt = app.padded(app.NEWLINE).join([
        app.escape('Current geometry (xyz format, in Angstrom)'),
        '',
        app.UNSIGNED_INTEGER,
        (app.one_or_more(app.NONNEWLINE) + app.SPACES +
         'ENERGY=' + app.FLOAT),
        ''
    ])

    syms, xyzs = ar.geom.read(
        output_str,
        start_ptt=ptt)
    geo = automol.geom.from_data(syms, xyzs, angstrom=True)

    return geo


def hess_geometry(output_str):
    """ Reads the optimized molecular geometry (in Cartesian coordinates) from
        the output file string that is associated with a Hessian calculation
        so that the two are in the same coordinate system.
        Returns the geometry in Bohr.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: automol molecular geometry data structure
    """

    syms, xyzs = ar.geom.read(
        output_str,
        start_ptt=app.padded(app.NEWLINE).join([
            app.escape('ATOMIC COORDINATES'),
            app.LINE, app.LINE, app.LINE, '']),
        line_start_ptt=app.UNSIGNED_INTEGER,
        line_sep_ptt=app.FLOAT,)
    geo = automol.geom.from_data(syms, xyzs, angstrom=False)

    return geo


def opt_zmatrix(output_str):
    """ Reads the optimized Z-Matrix from the output file string.
        Returns the Z-Matrix in Bohr and Radians.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: automol molecular geometry data structure
    """

    # Reads the matrix from the beginning of the output
    syms, key_mat, name_mat = ar.zmatrix.matrix.read(
        output_str,
        start_ptt=app.maybe(app.SPACES).join([
            'geometry', app.escape('='), app.escape('{'), '']),
        entry_start_ptt=app.maybe(','),
        entry_sep_ptt=',',
        last=False,
        case=False)

    # Read the initial z-matrix values from the beginning out the output
    if len(syms) == 1:
        val_dct = {}
    else:
        val_dct = ar.zmatrix.setval.read(
            output_str,
            # entry_start_ptt=MOLPRO_ENTRY_START_PATTERN,
            entry_start_ptt='SETTING',
            name_ptt=(
                app.one_of_these(['R', 'A', 'D']) +
                app.one_or_more(app.INTEGER)),
            val_ptt=(
                app.one_of_these([app.EXPONENTIAL_FLOAT_D, app.NUMBER])),
            last=True,
            case=False)

    names = sorted(set(numpy.ravel(name_mat)) - {None})
    caps_names = list(map(str.upper, names))
    name_dct = dict(zip(caps_names, names))
    assert set(caps_names) <= set(val_dct)
    val_dct = {name_dct[caps_name]: val_dct[caps_name]
               for caps_name in caps_names}

    # Read optimized z-matrix values from the end of the output
    var_string = app.one_of_these([
        app.padded('Optimized variables'),
        app.padded('Current variables')
    ])
    opt_val_dct = ar.zmatrix.setval.read(
        output_str,
        start_ptt=var_string + app.NEWLINE,
        entry_end_ptt=app.one_of_these(['ANGSTROM', 'DEGREE']),
        last=True,
        case=False)
    opt_val_dct = {name_dct[caps_name]: opt_val_dct[caps_name]
                   for caps_name in opt_val_dct.keys()}
    assert set(opt_val_dct) <= set(val_dct)
    val_dct.update(opt_val_dct)

    # Call the automol constructor
    zma = automol.zmatrix.from_data(
        syms, key_mat, name_mat, val_dct,
        one_indexed=True, angstrom=True, degree=True)
    return zma
