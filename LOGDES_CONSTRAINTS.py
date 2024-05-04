import LOGDES_Parameters, LOGDES_Variables, LOGDES_Sets
from pulp import LpProblem, LpConstraint, LpMinimize, LpVariable, lpSum, LpBinary, LpStatus, LpContinuous, PULP_CBC_CMD
from LOGDES_Variables import FLVI_ibs, FLVII_ibr, FLVIII_ibo, FLIII_bjt, FLIV_bje, FLI_ijt, FLII_ije, FLV_ibj, NUMI_ijt, NUMVII_ibr, NUMIII_bjt, P_b, lamda_j, W_ije, X_ijt, YIII_bjt, YIV_bje, ZVI_ibs, ZVII_ibr, ZVIII_ibo, L1_ije, L2_ijt, L3_bjt, L4_bje
from LOGDES_Parameters import M, bmax, TD_ij_dict, CAP_ir_dict, CAPP_it_dict, PC_i_dict, muy, CB_r_dict, CBB_t_dict, FC_b_dict, VCII_ije_dict, VCI_ijt_dict, VCIII_bjt_dict, VCIV_bje_dict, ENVI_s_dict, ENVII_b_dict, ENVIII_o_dict, ENVIV_e_dict, EMI_r_dict, EMII_t_dict, JOBI_s_dict, JOBII_b_dict, JOBIII_o_dict, JOBIV_e_dict, JOBV_r_dict, JOBVI_t_dict, d_ib_dict, d_ij_dict, d_bj_dict
from LOGDES_Sets import B, J, T, E, S, R, O, I

Constraints = []
# Flow and establishing of the whs constraints
for b in B:
    for j in J:
        for t in T:
            Constraints.append(LpConstraint(FLIII_bjt[b, j, t] <= P_b[b]*M))


#(5)
for b in B:
    for j in J:
        for e in E:
            Constraints.append(LpConstraint(FLIV_bje[b,j,e] <= P_b[b]*M))

#6
for i in I:
    for b in B:
        for s in S:
            Constraints.append(LpConstraint(FLVI_ibs[i,b,s] <= P_b[b]*M))

#7
for i in I:
    for b in B:
        for r in R:
            Constraints.append(LpConstraint(FLVII_ibr[i,b,r] <= P_b[b]*M))

#8
for i in I:
    for b in B:
        for o in O:
            Constraints.append(LpConstraint(FLVIII_ibo[i,b,o] <= P_b[b]*M))

#9
for b in B:
    Constraints.append(LpConstraint((lpSum(P_b[b] )) == bmax))


#Single allocation constraint
#(10)
for i in I:
    for b in B:
        for j in J:
            Constraints.append(LpConstraint(lpSum(W_ije[i, j, e] for e in E) + lpSum(X_ijt[i, j, t] for t in T) + lpSum(YIII_bjt[b, j, t] for t in T) + lpSum(YIV_bje[b, j, e] for e in E) == 1))

#Fulfillment of demand constraints
#(11)
for i in I:
    for j in J:
        Constraints.append(LpConstraint(lpSum(FLII_ije[i, j, e] for e in E) + lpSum(FLI_ijt[i, j, t] for t in T) + lpSum(FLV_ibj[i, b, j] for b in B) >= TD_ij_dict[i, j]))

#(12)
for i in I:
    for j in J:
        Constraints.append(LpConstraint(lpSum(FLII_ije[i, j, e]*PC_i_dict[i]  for e in E) + lpSum(FLI_ijt[i, j, t]*PC_i_dict[i] for t in T) + lpSum(FLV_ibj[i, b, j]*PC_i_dict[i] for b in B) <= (muy*lamda_j[j] + M*(1-lamda_j[j]))))

#Capacity vehicles constraints
#(13)
for i in I:
    for j in J:
        for t in T:
            Constraints.append(LpConstraint((FLI_ijt[i, j, t]) <= NUMI_ijt[i, j, t]*CAPP_it_dict[i, t]))
            Constraints.append(LpConstraint((NUMI_ijt[i, j, t]-1)*CAPP_it_dict[i, t] <= (FLI_ijt[i, j, t])))

#(14)
for i in I:
    for b in B:
        for r in R:
            Constraints.append(LpConstraint((FLVII_ibr[i, b, r]) <= NUMVII_ibr[i, b, r]*CAP_ir_dict[i, r]))
            Constraints.append(LpConstraint((NUMVII_ibr[i, b, r]-1)*CAP_ir_dict[i, r] <= (FLVII_ibr[i, b, r])))

#(15)
for i in I:
    for b in B:
        for j in J:
            for t in T:
                Constraints.append(LpConstraint(FLIII_bjt[b, j, t] <= NUMIII_bjt[b, j, t]*CAPP_it_dict[i, t]))
                Constraints.append(LpConstraint((NUMIII_bjt[b, j, t]-1)*CAPP_it_dict[i, t] <= FLIII_bjt[b, j, t]))


#Flow and allocation constraints:
#16
for i in I:
    for j in J:
        for e in E:
            Constraints.append(LpConstraint(FLII_ije[i,j,e] <= (W_ije[i,j,e]*M)))

#17
for i in I:
    for j in J:
        for t in T:
            Constraints.append(LpConstraint(FLI_ijt[i,j,t] <= (X_ijt[i,j,t]*M)))

#18
for b in B:
    for j in J:
        for t in T:
            Constraints.append(LpConstraint(FLIII_bjt[b,j,t] <= (YIII_bjt[b,j,t]*M)))

#19
for b in B:
    for j in J:
        for e in E:
            Constraints.append(LpConstraint(FLIV_bje[b,j,e] <= (YIV_bje[b,j,e]*M)))

#20

for i in I:
    for b in B:
        for s in S:
            Constraints.append(FLVI_ibs[i,b,s] <= (ZVI_ibs[i,b,s]*M))

#21

for i in I:
    for b in B:
        for r in R:
            Constraints.append(LpConstraint((ZVII_ibr[i,b,r]) <= (ZVII_ibr[i,b,r]*M)))

#22

for i in I:
    for b in B:
        for o in O:
            Constraints.append(LpConstraint(FLVIII_ibo[i,b,o] <= ZVIII_ibo[i,b,o]*M))


#Allocation and establishing of the warehouse constraints:
#23

for b in B:
    for j in J:
        for t in T:
            Constraints.append(LpConstraint(YIII_bjt[b,j,t] <= P_b[b]))

#24

for b in B:
    for j in J:
        for e in E:
            Constraints.append(LpConstraint(YIV_bje[b,j,e] <= P_b[b]))

#25

for i in I:
    for b in B:
        for s in S:
            Constraints.append(LpConstraint(ZVI_ibs[i,b,s] <= P_b[b]))

#26
for i in I:
    for b in B:
        for r in R:
            Constraints.append(LpConstraint(ZVII_ibr[i,b,r] <= P_b[b]))

#27

for i in I:
    for b in B:
        for r in R:
            Constraints.append(LpConstraint(ZVIII_ibo[i,b,o] <= P_b[b]))


#Flow balancing constraints
#(28)

for i in I:
    for b in B:
        for j in J:
            Constraints.append(LpConstraint((lpSum(FLVI_ibs[i, b, s] for s in S) + lpSum(FLVIII_ibo[i, b, o] for o in O) + lpSum(FLVII_ibr[i, b, r] for r in R)) == (lpSum(FLIII_bjt[b, j, t] for t in T) + lpSum(FLIV_bje[b, j, e] for e in E))))

#(29)

for i in I:
    for b in B:
        for j in J:
            Constraints.append(LpConstraint(((lpSum(FLVI_ibs[i, b, s] for s in S) + lpSum(FLVIII_ibo[i, b, o] for o in O) + lpSum(FLVII_ibr[i, b, r] for r in R) + lpSum(FLIII_bjt[b, j, t] for t in T) + lpSum(FLIV_bje[b, j, e] for e in E))/2 == FLV_ibj[i, b, j])))

# #Additional variables
# #(32)
# for i in I:
#     for j in J:
#         for e in E:
#             Constraints.append(LpConstraint((L1_ije[i, j, e]) == ((1 - lamda_j[j])*FLII_ije[i, j, e])))

# #(33)
# for i in I:
#     for j in J:
#         for t in T:
#             Constraints.append(LpConstraint((L2_ijt[i, j, t]) == ((1- lamda_j[j])*FLI_ijt[i, j, t])))

# #(34)

# for b in B:
#     for j in J:
#         for t in T:
#             Constraints.append(LpConstraint((L3_bjt[b, j, t]) == ((1- lamda_j[j])*FLIII_bjt[b, j, t])))

# #(35)

# for b in B:
#     for j in J:
#         for e in E:
#             Constraints.append(LpConstraint((L4_bje[b, j, e]) == ((1- lamda_j[j])*FLIV_bje[b, j, e])))

#Additonal constraints for new variables
#(37, 38, 39)

for i in I:
    for j in J:
        for e in E:
            Constraints.append(LpConstraint(L1_ije[i, j, e] <= (M*(1- lamda_j[j]) + FLII_ije[i, j, e])))
            Constraints.append(LpConstraint(L1_ije[i, j, e] >= (FLII_ije[i, j, e] + M*((1- lamda_j[j])-1))))
            Constraints.append(LpConstraint(L1_ije[i, j, e] <= M*(1- lamda_j[j])))

#(40, 41, 42)

for i in I:
    for j in J:
        for t in T:
            Constraints.append(LpConstraint(L2_ijt[i, j, t] <= (M*(1- lamda_j[j]) + FLI_ijt[i, j, t])))
            Constraints.append(LpConstraint(L2_ijt[i, j, t] >= (FLI_ijt[i, j, t] + M*((1- lamda_j[j])-1))))
            Constraints.append(LpConstraint(L2_ijt[i, j, t] <= M*(1- lamda_j[j])))

#(43, 44, 45)

for b in B:
    for j in J:
        for t in T:
            Constraints.append(LpConstraint(L3_bjt[b, j, t] <= (M*(1- lamda_j[j]) + FLIII_bjt[b, j, t])))
            Constraints.append(LpConstraint(L3_bjt[b, j, t] >= (FLIII_bjt[b, j, t] + M*((1- lamda_j[j])-1))))
            Constraints.append(LpConstraint(L3_bjt[b, j, t] <= M*(1- lamda_j[j])))

#(46, 47, 48)

for b in B:
    for j in J:
        for e in E:
            Constraints.append(LpConstraint(L4_bje[b, j, e] <= (M*(1- lamda_j[j]) + FLIV_bje[b, j, e])))
            Constraints.append(LpConstraint(L4_bje[b, j, e] >= (FLIV_bje[b, j, e] + M*((1- lamda_j[j])-1))))
            Constraints.append(LpConstraint(L4_bje[b, j, e] <= M*(1- lamda_j[j])))

# print(Constraints)