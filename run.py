###----------------------set up 
import pandas as pd
import os
import glob

###---------------------read, parse, & clean 
#find files 
files = glob.glob('exercise_input_data_public/*.tsv.gz')
#merge
df = pd.concat([pd.read_csv(f, sep='\t', compression='gzip') for f in files],ignore_index=True)
#update sample name
df.columns = [col.replace('HG10101', 'HG00101') for col in df.columns]

###------------------------count alleles
#col names
info_cols = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT']
sample_cols = [col for col in df.columns if col not in info_cols]

#count
allele_counts = []
for sample in sample_cols:
    # Split genotypes and count alleles
    genotypes = df[sample].str.split('|', expand=True).values.flatten()
    major_count = (genotypes == '0').sum()
    minor_count = (genotypes == '1').sum()
    allele_counts.append({
        'sample_id': sample,
        'major_count': major_count,
        'minor_count': minor_count
    })
#save file
pd.DataFrame(allele_counts).to_csv('allele_counts.tsv', sep='\t', index=False)

###-------------------- subset and save files 
#create output directory
os.makedirs('output', exist_ok=True)
#10 files based on last digts
for digit in range(10):
    #select ending digit
    digit_samples = [col for col in sample_cols if col[-1] == str(digit)]
    if digit_samples:
        #save
        subset = df[info_cols + digit_samples]
        subset.to_csv(f'output/{digit}.chr21.10000000_14999999.tsv.gz',
                     sep='\t', index=False, compression='gzip')

