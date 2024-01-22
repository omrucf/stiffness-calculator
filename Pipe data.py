import os
import math
import csv

elastic_modulus = 900
density = 0.96
pipe_length = 6000

pipe_mold = [600, 700, 800, 1000, 1218.5, 1600, 2000]
# pipe_mold = [2000];


ppwt = {27: 90, 34: 130, 42: 170, 54: 230, 65: 380, 75: 400, 90: 620, 110: 840}
flat_die = {
    110: [3, 4, 5],
    125: [3, 5, 6],
    135: [3, 4, 5, 6, 7],
    150: [5, 6, 7],
    180: [5, 7, 10],
}
cladding_die = {
    27: [3],
    34: [3, 4],
    42: [4, 5, 6],
    54: [4, 5, 6],
    65: [5, 6, 7],
    75: [5, 6, 7, 8],
    90: [6, 7, 8, 10],
    110: [6, 7, 8, 10],
}


required_Sn = [2, 4, 6, 8, 12, 16]
result = []

for pd in pipe_mold:
    for p, wall_thickness in flat_die.items():  # p: pmkd1
        for s1 in wall_thickness:  # pmhd1
            for ppd, pp_thickness in cladding_die.items():  # ppd: ppzjp
                for s4 in pp_thickness:  # bfmhd1
                    # Equations for Pipe Stiffness
                    pp_thickness = pp_thickness * 0.97
                    Y1 = s1 / 2.0
                    Y2 = s1 + s4 + 0.9 * ppd / 2.0
                    A1 = s1 * p
                    A2 = (0.9 * ppd / 2.0 + s4) ** 2 * math.pi - (
                        0.9 * ppd / 2.0
                    ) ** 2 * math.pi
                    H = (Y1 * A1 + Y2 * A2) / (A1 + A2)
                    Y11 = abs(H - Y1)
                    Y21 = abs(Y2 - H)
                    J1 = p * (s1) ** 3 / 12.0
                    J2 = (
                        math.pi
                        / 64.0
                        * ((0.9 * ppd + 2.0 * s4) ** 4 - (0.9 * ppd) ** 4)
                    )
                    J = (J1 + A1 * Y11**2 + J2 + A2 * Y21**2) / p
                    Sn = 1000.0 * J * elastic_modulus / pd**3 # JyxTxml , gdzj
                    # print(Y1, Y2, A1, A2);
                    # print(H, Y11, Y21, J1);
                    # print(J2, J);

                    # Equations for Pipe Weight
                    V1 = pd * math.pi * 20.0 * 150.0
                    V2 = pd * math.pi * 20.0 * 150.0
                    V3 = (
                        ((pd / 2.0 + s1) ** 2 - (pd / 2.0) ** 2) * math.pi * pipe_length
                    )
                    Sbf = ((ppd / 2.0 + s4) ** 2 - (ppd / 2.0) ** 2) * math.pi
                    Lpp = pipe_length / p * (pd + s1 * 2) * math.pi
                    V4 = Sbf * Lpp
                    W1 = V1 * density / 1000000.0
                    # jyxzd
                    W2 = V2 * density / 1000000.0
                    W3 = V3 * density / 1000000.0
                    W4 = V4 * density / 1000000.0
                    W = W1 + W2 + W3 + W4
                    Wk = ppwt[ppd] / 1000.0
                    Wp = Lpp * Wk / 1000.0
                    Wz = W1 + W2 + W3 + W4 + Wp
                    W0 = Wz - W2 / 2.0
                    pp_dist = p - ppd - s4 * 2.0
                    if math.trunc(Sn) in required_Sn:
                        # print (pd, '\t', p, '\t', s1, '\t', ppd, '\t', s4, '\t', round(Sn, 2), '\t', round(W0, 2));
                        # result.append(str(pd) + ',' + str(p) + ',' + str(s1) + ',' + str(ppd) + ',' + str(s4) + ',' + str(round(Sn, 2)) + ',' + str(round(W0, 2)))
                        t_list = [
                            pd,
                            p,
                            s1,
                            ppd,
                            s4,
                            round(Sn, 2),
                            round(W0, 2),
                            pp_dist,
                        ]
                        result.append(t_list)


print(result)

header = [
    "Pipe Diameter",
    "Flat Die",
    "Thickness",
    "PP Diameter",
    "PP Thickness",
    "SN",
    "Pipe Weight",
    "PP Distance",
]

fp = os.path.realpath(os.path.dirname(__file__))
os.chdir(fp)

with open("required_SN.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    # Add header to csv file
    writer.writerow(header)
    # Add list of lists as rows to the csv file
    writer.writerows(result)
