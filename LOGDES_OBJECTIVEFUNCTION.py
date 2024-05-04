import LOGDES_Sets, LOGDES_Variables, LOGDES_Parameters
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpBinary, LpStatus, LpContinuous, PULP_CBC_CMD, LpMaximize
from LOGDES_Variables import FLVI_ibs, FLVII_ibr, FLVIII_ibo, FLIII_bjt, FLIV_bje, FLI_ijt, FLII_ije, FLV_ibj, NUMI_ijt, NUMVII_ibr, NUMIII_bjt, P_b, lamda_j, W_ije, X_ijt, YIII_bjt, YIV_bje, ZVI_ibs, ZVII_ibr, ZVIII_ibo, L1_ije, L2_ijt, L3_bjt, L4_bje
from LOGDES_Parameters import M, bmax, TD_ij, CAP_ir_dict, CAPP_it_dict, PC_i_dict, muy, CB_r_dict, CBB_t_dict, FC_b_dict, VCII_ije_dict, VCI_ijt_dict, VCIII_bjt_dict, VCIV_bje_dict, ENVI_s_dict, ENVII_b_dict, ENVIII_o_dict, ENVIV_e_dict, EMI_r_dict, EMII_t_dict, JOBI_s_dict, JOBII_b_dict, JOBIII_o_dict, JOBIV_e_dict, JOBV_r_dict, JOBVI_t_dict, d_ib_dict, d_ij_dict, d_bj_dict
from LOGDES_Sets import B, J, T, E, S, R, O, I
def min_F1(P_b, NUMI_ijt, NUMIII_bjt, NUMVII_ibr, L1_ije, L2_ijt, L3_bjt, L4_bje):
    prob = LpProblem("Minimize_F1", LpMinimize)
    prob += (lpSum(FC_b_dict[b] * P_b[b] for b in B) + 
        lpSum(CBB_t_dict[t] * NUMI_ijt[i, j, t] for i in I for j in J for t in T) + 
        lpSum(CBB_t_dict[t]*NUMIII_bjt[b, j, t] for b in B for j in J for t in T) + 
        lpSum(CB_r_dict[r]*NUMVII_ibr[i, b, r]  for i in I for b in B for r in R) + 
        lpSum(VCII_ije_dict[i, j ,e]*L1_ije[i, j, e] for i in I for j in J for e in E) + 
        lpSum(VCI_ijt_dict[i, j, t]*L2_ijt[i, j, t] for i in I for j in J for t in T) + 
        lpSum(VCIII_bjt_dict[b, j, t]*L3_bjt[b, j, t] for b in B for j in J for t in T) + 
        lpSum(VCIV_bje_dict[b, j, e]*L4_bje[b, j, e] for b in B for j in J for e in E))
    return prob

def min_F2(P_b, FLII_ije, FLI_ijt, FLIII_bjt, FLIV_bje, FLVI_ibs, FLVII_ibr, FLVIII_ibo):
    prob = LpProblem("Minimize F2", LpMinimize)
    prob +=  (
        lpSum(ENVII_b_dict[b] * P_b[b] for b in B)
        + 365*(lpSum(ENVIV_e_dict[e]*d_ij_dict[i,j]*FLII_ije[i,j,e] for i in I for j in J for e in E)
        + lpSum(EMII_t_dict[t]*d_ij_dict[i,j]*FLI_ijt[i,j,t] for i in I for j in J for t in T)
        + lpSum(EMII_t_dict[t]*d_bj_dict[b,j]*FLIII_bjt[b,j,t] for b in B for j in J for t in T)
        + lpSum(ENVIV_e_dict[e]*d_bj_dict[b,j]*FLIV_bje[b,j,e] for b in B for j in J for e in E)
        + lpSum(ENVI_s_dict[s]*d_ib_dict[i,b]*FLVI_ibs[i,b,s] for i in I for b in B for s in S)
        + lpSum(EMI_r_dict[r]*d_ib_dict[i,b]*FLVII_ibr[i,b,r] for i in I for b in B for r in R)
        + lpSum(ENVIII_o_dict[o]*d_ib_dict[i,b]*FLVIII_ibo[i,b,o] for i in I for b in B for o in O))
        )
    return prob


def max_F3(P_b, NUMI_ijt, NUMIII_bjt, NUMVII_ibr, FLII_ije, FLIV_bje, FLVIII_ibo, FLVI_ibs):
    prob = LpProblem("Maximize F3", LpMaximize)
    prob += (lpSum(JOBII_b_dict[b]*P_b[b] for b in B)
        +lpSum(JOBVI_t_dict[t]*NUMI_ijt[i,j,t] for i in I for j in J for t in T)
        +lpSum(JOBVI_t_dict[t]*NUMIII_bjt[b,j,t] for b in B for j in J for t in T)
        +lpSum(JOBV_r_dict[r]*NUMVII_ibr[i,b,r] for i in I for b in B for r in R)
        + 365*(lpSum(JOBIV_e_dict[e]*FLII_ije[i,j,e] for i in I for j in J for e in E)
        +lpSum(JOBIV_e_dict[e]*FLIV_bje[b,j,e] for b in B for j in J for e in E)  
        +lpSum(JOBIII_o_dict[o]*FLVIII_ibo[i,b,o] for i in I for b in B for o in O)
        +lpSum(JOBI_s_dict[s]*FLVI_ibs[i,b,s] for i in I for b in B for s in S)))
    return prob

# print(min_F1())