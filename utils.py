#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 12:43:23 2020

@author: yangfanlu
"""
import numpy as np
import pandas as pd
import subprocess

def copy_to_clipboard(to_copy, sep='\t'):
    """ Copies an array into a string format that can be pasted in Excel
        Columns separated by \t, rows separated by \n """
    if isinstance(to_copy, str):
        output = to_copy
    elif isinstance(to_copy, (list, pd.DataFrame, pd.Series, np.ndarray)):
        if isinstance(to_copy, list):
            to_copy = np.array(to_copy)
        elif isinstance(to_copy, pd.DataFrame):
            to_copy = np.array([[''] + list(map(str, to_copy.columns))] +
                               [[idx] + list(to_copy.loc[idx]) for idx in to_copy.index])
        elif isinstance(to_copy, pd.Series):
            to_copy = to_copy.as_matrix()
        
        if len(to_copy.shape) == 1: # 1D array
            output = '\r\n'.join(to_copy.astype(str))
        else:
            line_strs = [sep.join(line.astype(str)).replace('\n', '') for line in to_copy]
            output = '\r\n'.join(line_strs)
    else:
        raise Exception('Input has type %s not implemented' %type(to_copy))
    # Copy to clipboard (MAC)
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))