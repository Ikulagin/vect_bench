
> data_all

for i in 8 16 32 64 128 256 512 1024 2048; do ./processing_results.py $i data_$i data_counters_$i data_ports_uops_$i; cat data_$i >> data_all; echo >> data_all; done
