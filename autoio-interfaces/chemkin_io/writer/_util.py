""" Format utilities
"""

# import numpy as np
import automol.geom


CKIN_TRANS_HEADER_STR = """! THEORETICAL TRANSPORT PROPERTIES
!
! (1) Shape, index denotes atom (0), linear molec. (1), nonlinear molec. (2);
! (2) Epsilon, the Lennard-Jones well depth, in K;
! (3) Sigma, the Lennard-Jones collision diameter, in Angstrom;
! (4) Mu, total dipole moment, in Debye;
! (5) Alpha, mean static polarizability, in Angstrom^3; and
! (6) Z_rot, rotational relaxation collision number at 298 K."""


def name_column_length(names):
    """ Set the width of the name column
    """

    maxlen = 0
    for name in names:
        maxlen = max(maxlen, len(name))
    maxlen = max(maxlen, 9)
    names_len = str(maxlen + 3)

    return names_len


def format_rxn_name(rxn):
    """ Receives a rxn and creates an appropriate string
        to be written in a Chemkin mech. Adds third body if applicable

        :param rxn: reaction names and third body
        :type rxn: tuple ((rct1, rct2), (prd1, prd2), (third_bod1,))
        :return rxn_name: formatted reaction name for writing in the mech
        :rtype: str
    """
    rcts = rxn[0]
    prds = rxn[1]
    thrbdy = rxn[2][0]

    # Convert to list if only one species
    if not isinstance(rcts, tuple):
        rcts = [rcts]
    if not isinstance(prds, tuple):
        prds = [prds]

    # Write the strings
    rct_str = ' + '.join(rcts)
    prd_str = ' + '.join(prds)

    # Add the +M or (+M) text if it is applicable
    if thrbdy is not None:
        rct_str += thrbdy
        prd_str += thrbdy

    if len(prds) < 3:
        join_sign = '='
    else:
        join_sign = '=>'

    rxn_name = f'{rct_str} {join_sign} {prd_str}'

    return rxn_name


def format_shape_idx(geo):
    """ Determine the shape index that signifies the overall
        molecular structure.

        :param geo: molecular geometry
        :type geo: automol.geom objects
        :rtype: int
    """

    if automol.geom.is_atom(geo):
        shape_idx = 0
    else:
        if automol.geom.is_linear(geo):
            shape_idx = 1
        else:
            shape_idx = 2

    return shape_idx
