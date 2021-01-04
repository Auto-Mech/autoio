""" psi4 writer module """

import os
import automol
from ioformat import build_mako_str
import elstruct.par
import elstruct.option
from elstruct.writer import fill
from elstruct.writer._psi4._par import REF_DCT, OPTION_EVAL_DCT


PROG = elstruct.par.Program.PSI4

# set the path to the template files
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(THIS_DIR, 'templates')


def write_input(job_key, geo, charge, mult, method, basis, orb_restricted,
                # molecule options
                mol_options=(),
                # machine options
                memory=1, comment='', machine_options=(),
                # theory options
                scf_options=(), casscf_options=(), corr_options=(),
                # generic options
                gen_lines=None,
                # job options
                job_options=(), frozen_coordinates=(), saddle=False):
    """ Write an input file string for an electronic structure calculation
        by processing all of the information and using it to fill in
        a Mako template of the input file.

        :param job_key: job contained in the input file
        :type job_key: str
        :param geo: cartesian or z-matrix geometry
        :type geo: tuple
        :param charge: molecular charge
        :type charge: int
        :param mult: spin multiplicity
        :type mult: int
        :param method: electronic structure method
        :type method: str
        :param basis: basis set
        :type basis: str
        :param orb_restricted: parameter designating if restriced refrence used
        :type orb_restricted: bool
        :param mol_options: options for the molecule block
        :type mol_options: tuple[str]
        ;param memory: memory in GB
        :type memory: int
        :param comment: a comment string to be placed at the top of the file
        :type comment: str
        :param machine_options: machine directives
            (num procs, num threads, etc.)
        :type machine_options: tuple[str]
        :param scf_options: scf method directives
        :type scf_options: tuple[str]
        :param casscf_options: casscf method directives
        :type casscf_options: tuple[str]
        :param corr_options: correlation method directives
        :type corr_options: tuple[str]
        :param job_options: geometry optimization routine directives
        :type job_options: tuple[str]
        :param frozen_coordinates: only with z-matrix geometries; list of
            coordinate names to freeze
        :type fozen_coordinates: tuple[str]
        :param saddle: parameter signifiying a saddle point calculation
        :type saddle: bool
        :param gen_lines: generic lines for the input file
        :type gen_lines: dict[idx:str]
    """

    frozen_dis_strs, frozen_ang_strs, frozen_dih_strs = (
        _frozen_coordinate_strings(geo, frozen_coordinates))

    reference = _reference(method, mult, orb_restricted)
    geo_str, zmat_val_str, _ = fill.geometry_strings(geo, frozen_coordinates)

    if not elstruct.par.Method.is_correlated(method):
        assert not corr_options

    scf_options = fill.evaluate_options(scf_options, OPTION_EVAL_DCT)
    casscf_options = fill.evaluate_options(casscf_options, OPTION_EVAL_DCT)
    job_options = fill.evaluate_options(job_options, OPTION_EVAL_DCT)

    if saddle:
        job_options += ('set full_hess_every 0', 'set opt_type ts',)

    psi4_method = elstruct.par.program_method_name(PROG, method)
    psi4_basis = elstruct.par.program_basis_name(PROG, basis)

    # Set the gen lines blocks
    if gen_lines is not None:
        gen_lines = '\n'.join(gen_lines[1]) if 1 in gen_lines else ''
    else:
        gen_lines = ''

    fill_dct = {
        fill.TemplateKey.COMMENT: comment,
        fill.TemplateKey.MEMORY: memory,
        fill.TemplateKey.MACHINE_OPTIONS: '\n'.join(machine_options),
        fill.TemplateKey.MOL_OPTIONS: '\n'.join(mol_options),
        fill.TemplateKey.CHARGE: charge,
        fill.TemplateKey.MULT: mult,
        fill.TemplateKey.GEOM: geo_str,
        fill.TemplateKey.ZMAT_VALS: zmat_val_str,
        fill.TemplateKey.BASIS: psi4_basis,
        fill.TemplateKey.METHOD: psi4_method,
        fill.TemplateKey.REFERENCE: reference,
        fill.TemplateKey.SCF_OPTIONS: '\n'.join(scf_options),
        fill.TemplateKey.CORR_OPTIONS: '\n'.join(corr_options),
        fill.TemplateKey.JOB_KEY: job_key,
        fill.TemplateKey.JOB_OPTIONS: '\n'.join(job_options),
        fill.TemplateKey.FROZEN_DIS_STRS: frozen_dis_strs,
        fill.TemplateKey.FROZEN_ANG_STRS: frozen_ang_strs,
        fill.TemplateKey.FROZEN_DIH_STRS: frozen_dih_strs,
        fill.TemplateKey.GEN_LINES: '\n'.join(gen_lines),
    }

    return build_mako_str(
        template_file_name='all.mako',
        template_src_path=TEMPLATE_DIR,
        template_keys=fill_dct)


# Helper functions
def _frozen_coordinate_strings(geo, frozen_coordinates):
    if not frozen_coordinates:
        dis_strs = ang_strs = dih_strs = ()
    else:
        coo_dct = automol.zmatrix.coordinates(geo, shift=1)
        assert all(coo_name in coo_dct for coo_name in frozen_coordinates)

        def _coordinate_strings(coo_names):
            frz_coo_names = [coo_name for coo_name in frozen_coordinates
                             if coo_name in coo_names]
            frz_coo_strs = tuple(' '.join(map(str, coo_keys))
                                 for frz_coo_name in frz_coo_names
                                 for coo_keys in coo_dct[frz_coo_name])
            return frz_coo_strs

        dis_strs = _coordinate_strings(
            automol.zmatrix.distance_names(geo))
        ang_strs = _coordinate_strings(
            automol.zmatrix.central_angle_names(geo))
        dih_strs = _coordinate_strings(
            automol.zmatrix.dihedral_angle_names(geo))
    return dis_strs, ang_strs, dih_strs
