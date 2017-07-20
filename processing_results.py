#!/home/ikulagin/opt/python-3.6.2/bin/python3

import pdb
import statistics
import json
import sys
import math

eps = 10e-11

test_results = ("jk_novec.json",
                "kj_novec.json",
                "jk_vec_k_no_gather.json",
                "jk_vec_k_gather.json",    
                "jk_vec_j.json",
                "jk_vec_jk_bcast.json",
                "jk_vec_jk_strided_1.json",
                "jk_vec_jk_strided_2.json",
                "kj_vec_j.json",
                "kj_vec_k.json",
                "kj_vec_k_no_gather.json",
                "kj_vec_kj_1.json",
                "kj_vec_kj_1_no_gather.json",
                "kj_vec_kj_2.json")

data_perf_counts = open(sys.argv[3], "w")
data_ports_uops = open(sys.argv[4], "w")

def lookup_perf_counts(median_t, results, file):
    for i in results:
        if math.fabs(median_t - i["time"]) <= eps:
            file.write(" ".join(str(j["value"]) for j in i["performance counters"]))

speedup_vector = [];
speedup_file = open(sys.argv[2], "w")
for i in test_results:
    data_file = open("results_" + sys.argv[1] + "/" + i)
    data = json.load(data_file)

    tmp1 =  statistics.median_high(
        map(lambda x: (x["time"]), data[0]["run_results"]));
    tmp2 =  statistics.median_high(
         map(lambda x: (x["time"]), data[1]["run_results"]));
    tmp3 =  statistics.median_high(
        map(lambda x: (x["time"]), data[2]["run_results"]));
    tmp4 =  statistics.median_high(
        map(lambda x: (x["time"]), data[3]["run_results"]));

    data_ports_uops.write(i + " ")
    lookup_perf_counts(tmp1, data[0]["run_results"], data_ports_uops)
    data_ports_uops.write(" ")
    lookup_perf_counts(tmp2, data[1]["run_results"], data_ports_uops)
    data_ports_uops.write("\n")
    
    data_perf_counts.write(i + " ")
    lookup_perf_counts(tmp3, data[2]["run_results"], data_perf_counts)
    data_perf_counts.write(" ")
    lookup_perf_counts(tmp4, data[3]["run_results"], data_perf_counts)
    data_perf_counts.write("\n")
    
    print (i)
    print ("exp 1")
    print ("time:",tmp1)
    print ("exp 2")
    print ("time:",tmp2)
    print ("exp 3")
    print ("time:",tmp3)
    print ("exp 4")
    print ("time:",tmp4)

    time = statistics.median_high([tmp1, tmp2, tmp3, tmp4]);
    print ("median time:", time);

    if i == test_results[1]:
        novec_time = time

    if i != test_results[1] and i != test_results[0]:
        s = novec_time / time
        speedup_vector.append(s)
        print ("speedup:", s)
        

    print()
    
print("vector = <", speedup_vector, ">")
speedup_file.write(sys.argv[1] + " " + " ".join(str(x) for x in speedup_vector))
data_file.close()
speedup_file.close()
data_perf_counts.close()
data_ports_uops.close()
del speedup_vector[:]
