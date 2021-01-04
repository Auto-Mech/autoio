""" orca4 writer module """

import os
from ioformat import build_mako_str
import elstruct.par
import elstruct.option
from elstruct.writer import fill
from elstruct.writer._orca4._par import REF_DCT, OPTION_EVAL_DCT

PROG = elstruct.par.Program.ORCA4

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

    reference = _reference(method, mult, orb_restricted)
    geo_str, zmat_var_val_str, zmat_const_val_str = fill.geometry_strings(
        geo, frozen_coordinates)

    _ = machine_options
    _ = casscf_options
    _ = job_options
    _ = zmat_var_val_str
    _ = zmat_const_val_str
    _ = gen_lines

    memory = memory * 1000.0

    if elstruct.par.Method.is_correlated(method):
        assert not corr_options

    orca4_method = elstruct.par.program_method_name(PROG, method)
    orca4_basis = elstruct.par.program_basis_name(PROG, basis)

    # in the case of Hartree-Fock, swap the method for the reference name
    if method == elstruct.par.Method.HF[0]:
        orca4_method = reference
        reference = ''

    numerical = False
    nprocs = 1
    coord_sys = 'xyz'

    if saddle:
        raise NotImplementedError

    fill_dct = {
        fill.TemplateKey.NPROCS: nprocs,
        fill.TemplateKey.NUMERICAL: numerical,
        fill.TemplateKey.COORD_SYS: coord_sys,
        fill.TemplateKey.MEMORY: memory,
        fill.TemplateKey.REFERENCE: reference,
        fill.TemplateKey.METHOD: orca4_method,
        fill.TemplateKey.BASIS: orca4_basis,
        fill.TemplateKey.SCF_OPTIONS: ','.join(scf_options),
        fill.TemplateKey.MOL_OPTIONS: ','.join(mol_options),
        fill.TemplateKey.COMMENT: comment,
        fill.TemplateKey.CHARGE: charge,
        fill.TemplateKey.MULT: mult,
        fill.TemplateKey.GEOM: geo_str,
        fill.TemplateKey.JOB_KEY: job_key,
    }

    return build_mako_str(
        template_file_name='all.mako',
        template_src_path=TEMPLATE_DIR,
        template_keys=fill_dct)
