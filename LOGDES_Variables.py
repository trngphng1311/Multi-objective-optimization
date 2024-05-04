from pulp import LpVariable, LpInteger, LpBinary
from LOGDES_Sets import I, J, S, B, O, E, R, T
# Type integer
FLVI_ibs = LpVariable.dicts('FLVI_ibs', [(i, b, s) for i in I for b in B for s in S], lowBound=0, cat='Integer')  # The amount of product shipped from supplier i to warehouse b by supplier distribution team s 
FLVII_ibr = LpVariable.dicts('FLVII_ibr', [(i, b, r) for i in I for b in B for r in R], lowBound=0, cat='Integer')  # The amount of product shipped from supplier i to warehouse b by retailer distribution team r
FLVIII_ibo = LpVariable.dicts('FLVIII_ibo', [(i, b, o) for i in I for b in B for o in O], lowBound=0, cat='Integer')  # The amount of product shipped from supplier i to warehouse b by 3pl o
FLIII_bjt = LpVariable.dicts('FLIII_bjt', [(b, j, t) for b in B for j in J for t in T], lowBound=0, cat='Integer')  # The amount of product shipped from warehouse b to customer j by retailer distribution team t
FLIV_bje = LpVariable.dicts('FLIV_bje', [(b, j, e) for b in B for j in J for e in E], lowBound=0, cat='Integer')  # The amount of product shipped from warehouse b to customer j by 3pl e
FLI_ijt = LpVariable.dicts('FLI_ijt', [(i, j, t) for i in I for j in J for t in T], lowBound=0, cat='Integer')  # The amount of product shipped from supplier i to customer j by retailer distribution team t
FLII_ije = LpVariable.dicts('FLII_ije', [(i, j, e) for i in I for j in J for e in E], lowBound=0, cat='Integer')  # The amount of product shipped from supplier i to customer j by 3pl e
FLV_ibj = LpVariable.dicts('FLV_ibj', [(i, b, j) for i in I for b in B for j in J], lowBound=0, cat='Integer')  # The amount of product shipped between supplier i, warehouse b and customer j
NUMI_ijt = LpVariable.dicts('NUMI_ijt', [(i, j, t) for i in I for j in J for t in T], lowBound=0, cat='Integer')  # The number of vehicles needed to transfer the product from supplier i to customer j by the retailer distribution team t
NUMVII_ibr = LpVariable.dicts('NUMVII_ibr', [(i, b, r) for i in I for b in B for r in R], lowBound=0, cat='Integer')  # The number of vehicles needed to deliver the product from supplier i to the warehouse b by the retailer distribution team r
NUMIII_bjt = LpVariable.dicts('NUMIII_bjt', [(b, j, t) for b in B for j in J for t in T], lowBound=0, cat='Integer')  # The number of vehicles needed to transfer the product from stock b to customer j by the retailer distribution team t

# Type Binary
P_b = LpVariable.dicts('P_b', B, cat='Binary')  # 1 if the warehouse b is to be established, and 0 otherwise
lamda_j = LpVariable.dicts('lamda_j', J, cat='Binary')  # 1 if the order price of customer j is less than μ, and 0 if the order price of customer j is more than μ
W_ije = LpVariable.dicts('W_ije', [(i, j, e) for i in I for j in J for e in E], cat='Binary')  # 1 if the supplier i is allocated to the customer j by 3pl e and 0 otherwise
X_ijt = LpVariable.dicts('X_ijt', [(i, j, t) for i in I for j in J for t in T], cat='Binary')  # 1 if the supplier i is allocated to the customer j by the retailer distribution team t, and 0 otherwise
YIII_bjt = LpVariable.dicts('YIII_bjt', [(b, j, t) for b in B for j in J for t in T], cat='Binary')  # 1 if the warehouse b is allocated to the customer j by the retailer distribution team t, and 0 otherwise
YIV_bje = LpVariable.dicts('YIV_bje', [(b, j, e) for b in B for j in J for e in E], cat='Binary')  # 1 if the warehouse b is allocated to the customer j by 3pl e, and 0 and otherwise
ZVI_ibs = LpVariable.dicts('ZVI_ibs', [(i, b, s) for i in I for b in B for s in S], cat='Binary')  # 1 if the supplier i is allocated to the warehouse b by the supplier distribution team s, and 0 otherwise
ZVII_ibr = LpVariable.dicts('ZVII_ibr', [(i, b, r) for i in I for b in B for r in R], cat='Binary')  # 1 if the supplier i is allocated to the warehouse b by the retailer distribution team r, and 0 otherwise
ZVIII_ibo = LpVariable.dicts('ZVIII_ibo', [(i, b, o) for i in I for b in B for o in O], cat='Binary')  # 1 if the supplier i is allocated to the warehouse b by 3pl p, and 0 otherwise

# Additional variables
L1_ije = LpVariable.dicts('L1_ije', [(i, j, e) for i in I for j in J for e in E], lowBound=0, cat='Integer')
L2_ijt = LpVariable.dicts('L2_ijt', [(i, j, t) for i in I for j in J for t in T], lowBound=0, cat='Integer')
L3_bjt = LpVariable.dicts('L3_bjt', [(b, j, t) for b in B for j in J for t in T], lowBound=0, cat='Integer')
L4_bje = LpVariable.dicts('L4_bje', [(b, j, e) for b in B for j in J for e in E], lowBound=0, cat='Integer')



