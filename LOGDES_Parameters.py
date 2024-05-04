import pandas as pd
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpBinary, LpStatus, LpContinuous, PULP_CBC_CMD
from LOGDES_Sets import B, J, T, E, S, R, O, I
from LOGDES_Variables import FLVI_ibs, FLVII_ibr, FLVIII_ibo, FLIII_bjt, FLIV_bje, FLI_ijt, FLII_ije, FLV_ibj, NUMI_ijt, NUMVII_ibr, NUMIII_bjt, P_b, lamda_j, W_ije, X_ijt, YIII_bjt, YIV_bje, ZVI_ibs, ZVII_ibr, ZVIII_ibo, L1_ije, L2_ijt, L3_bjt, L4_bje

#Export Data
file_path = 'C:/Users/Admin/OneDrive - VietNam National University - HCM INTERNATIONAL UNIVERSITY/Documents/PYTHON/MULTI-CHANNEL OPTIMIZATION PROB/VU_DATA.xlsx'

#Read data from excel file
Product = pd.read_excel(file_path, sheet_name="Product data", header=0) 
Cost = pd.read_excel(file_path, sheet_name="Cost data", header=0) 
Environment = pd.read_excel(file_path, sheet_name="Environmental data", header=0) 
Job = pd.read_excel(file_path, sheet_name="Job oppotunities", header=0)
Distance = pd.read_excel(file_path, sheet_name="Distance", header=0)

# Parameter Component - Ki hieu giong torng research nhe, co ki hieu nao kh ghi ra duoc hay co thay doi thi bao de cao nhap nhe 
M = 10000      #Large real number 10^99
bmax = 7       #Maximum number of warehouses allowed to build
TD_ij = Product.iloc[2:12, 1:6].values.tolist()     #The demand amount of customer j from supplier i 
CAP_ir = Product.iloc[15:20, 1:4].values.tolist()    #Capacity of retailer distribution team r vehicle for supplier product i
CAPP_it = Product.iloc[15:20, 7:9].values.tolist()  #Capacity of retailer distribution team t vehicle for supplier product i
PC_i = Product.iloc[22:27, 1:2].values.tolist()      #Product price i
muy = 65       #The price level for free shipping
CB_r = Product.iloc[22:25, 4:5].values.tolist()      #Cost of purchasing vehicle retailer distribution team r
CBB_t = Product.iloc[22:24, 7:8].values.tolist()     #Cost of purchasing vehicle retailer distribution team t
FC_b = Product.iloc[22:26, 10:11].values.tolist()      #Fixed cost of establishing a warehouse b
# print(FC_b)
VCII_ije = []  #Shipping cost of product flow from supplier i to customer j by 3pl e for free shipping if customer j purchases more than muy
#With e = 1
VCII_ij1 = []
for j in range(3, 13):
    e1_row = []
    for i in range(1, 6):
        value = Cost.iloc[j, i]
        e1_row.append(value)
    VCII_ij1.append(e1_row)
VCII_ije.append(VCII_ij1)
#With e = 2
VCII_ij2 = []
for j in range(18, 28):
    e2_row = []
    for i in range(1, 6):
        value = Cost.iloc[j, i]
        e2_row.append(value)
    VCII_ij2.append(e2_row)
VCII_ije.append(VCII_ij2)

VCI_ijt = []   #Shipping cost of product flow from supplier i to customer j by retailer distribution team t for free shipping if customer j purchases more than muy
#With t = 1
VCI_ij1 = []
for j in range(32, 42):
    row_t1 = []
    for i in range(1, 6):
        value_t1 = Cost.iloc[j, i]
        row_t1.append(value_t1)
    VCI_ij1.append(row_t1)
VCI_ijt.append(VCI_ij1) 
#With t = 2
VCI_ij2 = []
for j in range(46, 56):
    row_t2 = []
    for i in range(1, 6):
        value_t1 = Cost.iloc[j, i]
        row_t2.append(value_t1)
    VCI_ij2.append(row_t2)
VCI_ijt.append(VCI_ij2) 

VCIII_bjt = [] #The cost of transporting product flow from warehouse b to customer j by the retail distribution team t for free shipping if customer j purchases more than muy
#With t = 1
VCIII_bj1 = []
for j in range(3, 13):
    row_t11 = []
    for i in range(8, 13):
        value_tt = Cost.iloc[j, i]
        row_t11.append(value_tt)
    VCIII_bj1.append(row_t11)
VCIII_bjt.append(VCIII_bj1)
#With t = 2
VCIII_bj2 = []
for j in range(18, 28):
    row_t22 = []
    for i in range(8, 13):
        value_tt = Cost.iloc[j, i]
        row_t22.append(value_tt)
    VCIII_bj2.append(row_t22)
VCIII_bjt.append(VCIII_bj2)

VCIV_bje = []  #The cost of transporting product flow from warehouse b to customer j by 3pl e for free shipping if customer j purchases more than muy
#With t = 1
VCIV_bj1 = []
for j in range(3, 13):
    row_e11 = []
    for i in range(15, 20):
        value_ee = Cost.iloc[j, i]
        row_e11.append(value_ee)
    VCIV_bj1.append(row_e11)
VCIV_bje.append(VCIV_bj1)
#With t = 2
VCIV_bj2 = []
for j in range(18, 28):
    row_e22 = []
    for i in range(15, 20):
        value_ee = Cost.iloc[j, i]
        row_e22.append(value_ee)
    VCIV_bj2.append(row_e22)
VCIV_bje.append(VCIV_bj2)

ENVI_s = Environment.iloc[2:5, 1:2].values.tolist()     #Environmental impacts of the supplier distribution team s
ENVII_b = Environment.iloc[2:6, 4:5].values.tolist()   #Environmental impacts of establishing potential warehouse b
ENVIII_o = Environment.iloc[2:4, 7:8].values.tolist()   #Environmental impacts of 3pl o
ENVIV_e = Environment.iloc[2:4, 10:11].values.tolist()    #Environmental impacts of 3pl e
EMI_r = Environment.iloc[9:12, 1:2].values.tolist()      #Carbon di-oxide emission factor of vehicle retailer distribution team r
EMII_t = Environment.iloc[9:11, 4:5].values.tolist()    #Carbon di-oxide emission factor of vehicle retailer distribution team t
JOBI_s = Job.iloc[1:4, 1:2].values.tolist()     #The number of job opportunities created by the supplier distribution team s
JOBII_b = Job.iloc[1:5, 4:5].values.tolist()     #The number of fixed job opportunities created by establishing potential warehouse b
JOBIII_o = Job.iloc[1:3, 7:8].values.tolist()   #The number of job opportunities created by 3pl o
JOBIV_e = Job.iloc[1:3, 10:11].values.tolist()     #The number of job opportunities created by 3pl e
JOBV_r = Job.iloc[1:4, 13:14].values.tolist()      #The number of job opportunities created by vehicle retailer distribution team r
JOBVI_t = Job.iloc[1:3, 16:17].values.tolist()     #The number of job opportunities created by vehicle retailer distribution team t
d_ib = Distance.iloc[2:7, 1:5].values.tolist()       #The distance between supplier i and warehouse b
d_ij = Distance.iloc[10:15, 1:11].values.tolist()       #The distance between supplier i and customer j
d_bj = Distance.iloc[18:28, 1:5].values.tolist()       #The distance between warehouse b and customer j

# Convert lists into dictionaries
PC_i_dict = {i: price[0] for i, price in enumerate(PC_i)}
CAP_ir_dict = {(i, r): cap for i, row in enumerate(CAP_ir) for r, cap in enumerate(row)}
CAPP_it_dict = {(i, t): cap for i, row in enumerate(CAPP_it) for t, cap in enumerate(row)}
CB_r_dict = {r: cost[0] for r, cost in enumerate(CB_r)}
CBB_t_dict = {t: cost[0] for t, cost in enumerate(CBB_t)}
FC_b_dict = {b: cost[0] for b, cost in enumerate(FC_b)}
VCII_ije_dict = {(i, j, e): cost for e, matrix in enumerate(VCII_ije) for j, row in enumerate(matrix) for i, cost in enumerate(row)}
VCI_ijt_dict = {(i, j, t): cost for t, matrix in enumerate(VCI_ijt) for j, row in enumerate(matrix) for i, cost in enumerate(row)}
VCIII_bjt_dict = {(b, j, t): cost for t, matrix in enumerate(VCIII_bjt) for j, row in enumerate(matrix) for b, cost in enumerate(row)}
VCIV_bje_dict = {(b, j, e): cost for e, matrix in enumerate(VCIV_bje) for j, row in enumerate(matrix) for b, cost in enumerate(row)}
ENVI_s_dict = {s: impact[0] for s, impact in enumerate(ENVI_s)}
ENVII_b_dict = {b: impact[0] for b, impact in enumerate(ENVII_b)}
ENVIII_o_dict = {o: impact[0] for o, impact in enumerate(ENVIII_o)}
ENVIV_e_dict = {e: impact[0] for e, impact in enumerate(ENVIV_e)}
EMI_r_dict = {r: emission[0] for r, emission in enumerate(EMI_r)}
EMII_t_dict = {t: emission[0] for t, emission in enumerate(EMII_t)}
JOBI_s_dict = {s: jobs[0] for s, jobs in enumerate(JOBI_s)}
JOBII_b_dict = {b: jobs[0] for b, jobs in enumerate(JOBII_b)}
JOBIII_o_dict = {o: jobs[0] for o, jobs in enumerate(JOBIII_o)}
JOBIV_e_dict = {e: jobs[0] for e, jobs in enumerate(JOBIV_e)}
JOBV_r_dict = {r: jobs[0] for r, jobs in enumerate(JOBV_r)}
JOBVI_t_dict = {t: jobs[0] for t, jobs in enumerate(JOBVI_t)}
TD_ij_dict = {(i, j): dist for j, row in enumerate(TD_ij) for i, dist in enumerate(row)} 
d_ib_dict = {(i, b): dist for i, row in enumerate(d_ib) for b, dist in enumerate(row)}
d_ij_dict = {(i, j): dist for i, row in enumerate(d_ij) for j, dist in enumerate(row)}
d_bj_dict = {(b, j): dist for j, row in enumerate(d_bj) for b, dist in enumerate(row)} #b la j, j la b 


# print(CAPP_it_dict)
