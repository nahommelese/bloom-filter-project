import argparse,csv
from pathlib import Path
from bloom_filter import BloomFilter
from experiments.common import RESULTS_DATA, generate_words

def parse(raw): return [float(x) for x in raw.split(',') if x.strip()]
def run(expected_items,target_fpr,load_factors,query_count,output):
    rows=[]
    for load in load_factors:
        count=round(expected_items*load); inserted=generate_words(count,1000+count); absent=generate_words(query_count,2000+count)
        bloom=BloomFilter(expected_items,target_fpr); bloom.update(inserted); fp=sum(x in bloom for x in absent)
        rows.append({'expected_items':expected_items,'inserted_items':count,'load_factor':load,'query_count':query_count,'false_positives':fp,'observed_false_positive_rate':fp/query_count,'estimated_false_positive_rate':bloom.estimated_false_positive_rate(),'fill_ratio':bloom.fill_ratio,'bit_count':bloom.bit_count,'hash_count':bloom.hash_count})
    with output.open('w',newline='',encoding='utf-8') as h:
        w=csv.DictWriter(h,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--expected-items',type=int,default=100000); p.add_argument('--target-fpr',type=float,default=0.01); p.add_argument('--load-factors',default='0.25,0.5,0.75,1,1.25,1.5,2,3'); p.add_argument('--query-count',type=int,default=100000); p.add_argument('--output',type=Path,default=RESULTS_DATA/'hpc_false_positive_rate.csv'); a=p.parse_args(); run(a.expected_items,a.target_fpr,parse(a.load_factors),a.query_count,a.output); print('Wrote',a.output)
