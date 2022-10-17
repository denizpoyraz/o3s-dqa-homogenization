import pandas as pd
import numpy as np
import glob
from datetime import datetime
from re import search

from nilu_ndacc.read_nilu_functions import ComputeCef, VecInterpolate
from functions.homogenization_functions import VecInterpolate_linear, VecInterpolate_log


VecP_ECC6A = [0, 2, 3, 5, 10, 20, 30, 50, 100, 200, 300, 500, 1000, 1100]
VecC_ECC6A_30 = [1.171, 1.171, 1.131, 1.092, 1.055, 1.032, 1.022, 1.015, 1.011, 1.008, 1.006, 1.004, 1, 1]

rVecP_ECC6A = [0, 2, 3, 5, 10, 20, 30, 50, 100, 200, 300, 500, 1000, 1100]
rVecC_ECC6A_30 = [1.171, 1.171, 1.131, 1.092, 1.055, 1.032, 1.022, 1.015, 1.011, 1.008, 1.006, 1.004, 1, 1]

pval_va = rVecP_ECC6A
pval_va.reverse()
vec_spc = rVecC_ECC6A_30
vec_spc.reverse()
vec_spc_unc = [0.001]* len(pval_va)

pval = np.array([1100, 200, 100, 50, 30, 20, 10, 7, 5, 3])
pvallog = [np.log10(i) for i in pval]
print(pvallog)

komhyr_86 = np.array([1, 1, 1.007, 1.018, 1.022, 1.032, 1.055, 1.070, 1.092, 1.124])  # SP Komhyr
komhyr_86_unc = np.array([0, 0, 0.005, 0.006, 0.008, 0.009, 0.010, 0.012, 0.014, 0.025])  # SP Komhyr


dft = pd.read_hdf('/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/Current/upd2_ny950309_rawcurrent.hdf')



dft['Cef_vlin'] = VecInterpolate(VecP_ECC6A, VecC_ECC6A_30, dft, 0)
dft['Cef_klog'], dft['unc_Cpf'] = VecInterpolate_log(pvallog, komhyr_86, komhyr_86_unc, dft, "Pair")
dft['Cef_klin'], dft['unc_Cpf'] = VecInterpolate_linear(pval, komhyr_86, komhyr_86_unc, dft, "Pair")
dft['Cef_vlin2'], dft['unc_Cpf'] = VecInterpolate_linear(pval_va, vec_spc, vec_spc_unc, dft, "Pair")

dft.to_csv('/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/Current/test_ny950309_rawcurrent.hdf')