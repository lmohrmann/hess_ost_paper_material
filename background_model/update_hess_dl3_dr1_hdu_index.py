import numpy as np
from astropy.table import Table, Column, join
from shutil import copyfile
import os
import sys

# Input paths
bkg_model_path = sys.argv[1]
hess_dr1_path = sys.argv[2]

# Read in tables
obs_file = os.path.join(hess_dr1_path, 'obs-index.fits.gz')
hdu_file = os.path.join(hess_dr1_path, 'hdu-index.fits.gz')
obs_table = Table.read(str(obs_file), hdu='OBS_INDEX')
hdu_table = Table.read(str(hdu_file), hdu='HDU_INDEX')

# Read obs_ids
observations  = obs_table.field('OBS_ID')

# Loop over all observations
rows = []
for obs_id in observations:
    # Copy background files
    file_name = 'hess_bkg_3d_{:06d}.fits.gz'.format(obs_id)
    file_src = os.path.join(bkg_model_path, 'data', file_name)
    file_dest = os.path.join(hess_dr1_path, 'data', file_name)
    copyfile(file_src, file_dest)

    # Fill columns for hdu table
    data = []
    data.append(obs_id)
    data.append('bkg')
    data.append('bkg_3d')

    data.append('data')
    data.append(file_name)
    data.append('BACKGROUND')

    stat = os.stat(file_dest)
    data.append(stat.st_size)

    # Append data to rows list
    rows.append(data)

# Dump rows to table object and merge with original hdu-table
table = Table(rows=rows, names=hdu_table.colnames)
joined_hdu_table = join(hdu_table, table, join_type='outer')

# Write new hdu index file
hdu_file_bg = os.path.join(hess_dr1_path, 'hdu-index-bkg.fits.gz')
joined_hdu_table.write(hdu_file_bg, overwrite=True)
