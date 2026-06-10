import argparse,csv
from pathlib import Path
from bloom_filter import BloomFilter
from experiments.common import RESULTS_DATA
def ints(raw): return [int(x) for x in raw.split(',') if x.strip()]
def floats(raw): return [float(x) for x in raw.split(',') if x.strip()]
def run(sizes,fprs,avg_bytes,output):
    rows=[]
    for n in sizes:
        raw=n*avg_bytes
        for p in fprs:
            b=BloomFilter(n,p); rows.append({'expected_items':n,'target_false_positive_rate':p,'average_item_bytes_baseline':avg_bytes,'raw_storage_bytes_baseline':raw,'bloom_memory_bytes':b.memory_bytes,'bit_count':b.bit_count,'hash_count':b.hash_count,'compression_ratio_raw_divided_by_bloom':raw/b.memory_bytes,'bloom_size_as_fraction_of_raw':b.memory_bytes/raw})
    with output.open('w',newline='',encoding='utf-8') as h:
        w=csv.DictWriter(h,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--expected-sizes',default='1000,10000,100000,1000000'); p.add_argument('--target-fprs',default='0.1,0.05,0.01,0.001'); p.add_argument('--average-item-bytes',type=int,default=16); p.add_argument('--output',type=Path,default=RESULTS_DATA/'hpc_compression_rate.csv'); a=p.parse_args(); run(ints(a.expected_sizes),floats(a.target_fprs),a.average_item_bytes,a.output); print('Wrote',a.output)
