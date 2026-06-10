import argparse,csv
from collections import Counter
from pathlib import Path
from bloom_filter import BloomFilter
from experiments.common import RESULTS_DATA, generate_words, generate_dna
def distribution(values,buckets):
    bloom=BloomFilter(len(values),0.01); c=Counter()
    for v in values:
        for p in bloom.hash_positions(v): c[p % buckets]+=1
    return c
def run(count,buckets,output):
    rows=[]
    for typ,vals in [('words',generate_words(count,1)),('dna',generate_dna(count,2))]:
        c=distribution(vals,buckets)
        for b in range(buckets): rows.append({'data_type':typ,'bucket':b,'count':c[b]})
    with output.open('w',newline='',encoding='utf-8') as h:
        w=csv.DictWriter(h,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--item-count',type=int,default=50000); p.add_argument('--bucket-count',type=int,default=50); p.add_argument('--output',type=Path,default=RESULTS_DATA/'hpc_hash_distribution.csv'); a=p.parse_args(); run(a.item_count,a.bucket_count,a.output); print('Wrote',a.output)
