${globkey_str}


!===================================================
!  BEGIN MASTER EQUATION MODEL
!===================================================

Model
% if energy_trans_str is not None:

!---------------------------------------------------
!  ENERGY TRANSFER SECTION
!---------------------------------------------------
${energy_trans_str}

% endif
% if well_lump_str is not None:

!---------------------------------------------------
!  WELL LUMPING SECTION
!---------------------------------------------------
${well_lump_str}

% endif
!---------------------------------------------------
!  REACTION CHANNELS SECTION
!---------------------------------------------------
${rxn_chan_str}
End  ! Model

!===================================================
!  END MASTER EQUATION MODEL
!===================================================
