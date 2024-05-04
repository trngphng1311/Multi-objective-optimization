import pulp
from pulp import LpProblem, LpMinimize
from LOGDES_OBJECTIVEFUNCTION import min_F1, min_F2, max_F3
from LOGDES_Variables import FLVI_ibs, FLVII_ibr, FLVIII_ibo, FLIII_bjt, FLIV_bje, FLI_ijt, FLII_ije, FLV_ibj, NUMI_ijt, NUMVII_ibr, NUMIII_bjt, P_b, lamda_j, W_ije, X_ijt, YIII_bjt, YIV_bje, ZVI_ibs, ZVII_ibr, ZVIII_ibo, L1_ije, L2_ijt, L3_bjt, L4_bje
from LOGDES_CONSTRAINTS import Constraints


# Create the main problem
OBF = LpProblem("Main Problem", LpMinimize)

# Add objective functions with weights
OBF_F1 = LpProblem("Main Problem - F1", LpMinimize)
OBF_F1 += min_F1(P_b, NUMI_ijt, NUMIII_bjt, NUMVII_ibr, L1_ije, L2_ijt, L3_bjt, L4_bje).objective
for each_constraint in Constraints:
    OBF_F1 += each_constraint
OBF_F1.solve()

OBF_F2 = LpProblem("Main Problem - F2", LpMinimize)
OBF_F2 += min_F2(P_b, FLII_ije, FLI_ijt, FLIII_bjt, FLIV_bje, FLVI_ibs, FLVII_ibr, FLVIII_ibo).objective
for each_constraint in Constraints:
    OBF_F2 += each_constraint
OBF_F2.solve()

OBF_F3 = LpProblem("Main Problem - F3", LpMinimize)  # Change LpMaximize to LpMinimize
OBF_F3 += -max_F3(P_b, NUMI_ijt, NUMIII_bjt, NUMVII_ibr, FLII_ije, FLIV_bje, FLVIII_ibo, FLVI_ibs).objective  # Change the sign of the objective function
for each_constraint in Constraints:
    OBF_F3 += each_constraint
OBF_F3.solve()

# Solve the problem with the default solver
OBF.solve()

# Print the status of the solutions
print("Status of OBF_F1:", pulp.LpStatus[OBF_F1.status])
print("Status of OBF_F2:", pulp.LpStatus[OBF_F2.status])
print("Status of OBF_F3:", pulp.LpStatus[OBF_F3.status])
print("Status of OBF:", pulp.LpStatus[OBF.status])

# Print the optimal values of the objective functions
print("Optimal Values of Objective Functions:")
print(f"F1 = {min_F1(P_b, NUMI_ijt, NUMIII_bjt, NUMVII_ibr, L1_ije, L2_ijt, L3_bjt, L4_bje).objective.value()}")
print(f"F2 = {min_F2(P_b, FLII_ije, FLI_ijt, FLIII_bjt, FLIV_bje, FLVI_ibs, FLVII_ibr, FLVIII_ibo).objective.value()}")
print(f"F3 = {max_F3(P_b, NUMI_ijt, NUMIII_bjt, NUMVII_ibr, FLII_ije, FLIV_bje, FLVIII_ibo, FLVI_ibs).objective.value()}")

# Print the optimal values of the decision variables (excluding __dummy)
print("Optimal Values of Decision Variables (excluding __dummy):")
for v in OBF.variables():
    if v.name != '__dummy':
        print(f"{v.name}: {v.varValue}")