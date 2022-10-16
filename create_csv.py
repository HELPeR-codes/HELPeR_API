import pandas as pd

train_file_path = '/Users/khushboo/Downloads/ir_csv_path'


file = open(train_file_path, 'r', encoding='utf8')
# df = pd.read_csv("")
from datetime import datetime
date_updated = datetime.now()
df = pd.DataFrame({})
for line in file:
    # print(line)
    conceptfile = line.replace("\n", "")
    dftemp= pd.read_json(open(conceptfile),lines=True)
    if len(dftemp) > 0:
        dftemp = dftemp.sort_values(["overall_score"]).head(10)
        dftemp['resource_id'] = line.split("/")[-1].replace(".txt","").replace(".html","").replace(".concept.json","")
        df = pd.concat([df,dftemp],ignore_index=True)

df['is_active'] = 1
df['data_created'] = datetime.strftime(date_updated, "%d/%m/%y %H:%M")
df['update_date'] = datetime.strftime(date_updated, "%d/%m/%y %H:%M")
df['owner'] = 'machine'
df['update_action'] = 'added'
df['change_field'] = None



df = df.reset_index(drop=True)

concepts_to_remove = ['speci','theset','twen','harry potter','pride'
    ,'internet','expression','finding out','library','asimage','foa','aaai press', 'aat', 'aban', 'abe', 'abit', 'abra', 'abracadabra', 'abracadabra', 'abracadabra', 'abracadabra', 'abracadabra', 'abstrac', 'ac', 'ac', 'academic press', 'academic press', 'acedb', 'acm', 'acm computing surveys', 'acm computing surveys', 'acm press', 'acronym', 'act', 'actu', 'acxiom', 'adap', 'adata', 'adata', 'adcs', 'add', 'add', 'add', 'adap', 'adata', 'adata', 'adcs', 'add', 'add', 'add', 'add', 'addiction', 'adds', 'adds', 'adds', 'adds', 'adds', 'adds', 'adds', 'adds', 'advan', 'aerodynamics', 'aesthetics', 'affix', 'african american', 'agap', 'agap', 'agrawal', 'ai', 'ai complete', 'ai magazine', 'ais', 'al bernstein', 'al dean', 'al garcia', 'al garcia', 'al hart', 'al lee', 'al lee', 'al richardson', 'al roberts', 'al spink', 'alarum', 'alchemy', 'algorithm', 'algo', 'alice', 'alistair moffat', 'allais paradox', 'alldata', 'allsorts', 'alltheweb', 'alltheweb', 'alphabet', 'amdahl', 'amherst', 'amortized', 'amtrak', 'animage', 'aod', 'ap', 'apc', 'apostrophe', 'append', 'apple', 'apple cake', 'apple crisp', 'arith', 'arxiv', 'asian', 'asis', 'asphere', 'aspirin', 'aspx', 'assignment problem', 'assumption', 'astatic', 'astable', 'ata', 'atari', 'atf', 'atl', 'auto insurance', 'automat', 'avail', 'barber', 'basic belief', 'basic books', 'basics', 'bast', 'bcr', 'beaufays', 'beaulieu', 'because news', 'beef', 'beijing', 'berry', 'bhagavathy', 'bible', 'bimbo', 'binary', 'bourne', 'breast cancer', 'bridge', 'bridge', 'bridge', 'brill', 'brill', 'brill', 'café', 'callan', 'cambridge', 'cambridge university', 'cambridge university press', 'can', 'cancer', 'canet', 'cap', 'car insurance', 'card catalog', 'carnegie', 'carrot', 'case', 'cation', 'cbe', 'cbr', 'cd', 'cd', 'cd', 'cd', 'cd', 'cd', 'cda', 'cea', 'cen', 'cen', 'cen', 'cen', 'ceo', 'ceo', 'cess', 'cess', 'cess', 'cess', 'cess', 'cet', 'cf', 'cgm', 'chal', 'chapter book', 'chapter two', 'char', 'chase', 'chicago', 'chen chen', 'chemistry', 'chinese', 'chinese character', 'chinese characters', 'chr', 'circle', 'circus', 'cis', 'cision', '', 'citeseer', 'city', 'class es', 'class es', 'class es', 'class es', 'classic text', 'classic text', 'classical', 'classical', 'classical', 'classical', 'classical', 'classical', 'classical', 'classical', 'classical', 'classical', 'clause', 'cliché', 'cloud', 'cluster a', 'clu', 'cm', 'cmu', 'cmu', 'cocoa butter', 'coffee', 'coin', 'coma', 'command', 'commer', 'commodity', 'communication', 'communications of the acm', 'compact', 'compo', 'computer', 'concatenation', 'congress', 'copper', 'cornell university', 'cours de linguistique générale', 'cpc', 'cpl', 'cracker', 'credit card', 'credit card number', 'cri', 'critical role', 'critical vocabulary', 'croft', 'cu', 'cued recall', 'cur', 'curacy', 'curate', 'curate', 'curly brackets', 'currency', 'currency', 'currency', 'current contents', 'current contents', 'current literature', 'current literature', 'curvature', 'curvature', 'curvature', 'cwe', 'cwru', 'dard', 'dashed', 'dat', 'dav', 'dean', 'demon', 'denver', 'derive', '', 'ac', 'mp', 'li', 'rm', 'ql', 'np', 'sd', 'rt', 'pj', 'tt', 'ls', 'iq', 'vc', 'gy', 'rf', 'vr', 'lf', 'ai', 'ig', 'it', 'vm', 'ml', 'xa', 'kb', 'gb', 'mb', 'ox', 'vb', 'xp', 'hm', 'go', 'tu', 'qi', 'ra', 'ss', 'ck', 'lm', 'ec', 'cj', 'nn', 'xj', 'cm', 'fn', 'mk', 'dn', 'tk', 'mu', 'ng', 'ix', 'uk', 'wc', 'mj', 'yj', 'cf', 'cd', 'cu', 'kj', 'oc', 'wu', 'ul', 'bt', 'nt', 'ij', 'oj', 'kn', 'tl', 'ps', 'tp', 'bi', 'mf', 'xf', 'fj', 'kd', 'lb', 'ua', 'ti', 'dl', 'sn', 'jd', 'jp', 'jj', 'qs', 'kx', 'lw', 'xk', 'lp', 'oo', 'ap', 'dm', 'sj', 'pop', 'lan', 'ing', '', 'ful', 'cap', 'pri', 'pea', 'tem', 'dog', 'pdf', 'acm', 'nba', 'psu', 'sev', 'nrm', 'typ', 'mix', 'gto', 'lis', 'err', 'fea', 'iis', 'yan', 'acl', 'sun', 'ral', 'pow', 'hui', 'mod', 'sug', 'npr', 'hue', 'ona', 'ltm', 'fig', 'dfg', 'apc', 'sem', 'ime', 'tee', 'iam', 'sql', 'tos', 'pho', 'cur', 'ter', 'phe', 'ket', 'rss', 'thc', 'heo', 'rer', 'trf', 'rng', 'ici', 'ige', 'urs', 'urr', 'lvl', 'iav', 'iai', 'rpl', 'pir', 'rne', 'nic', 'cst', 'lvn', 'ror', 'icl', 'ioc', 'hir', 'ivr', 'siq', 'rnr', 'iot', 'tir', 'htr', 'ial', 'ert', 'nri', 'sis', 'ery', 'gps', 'spa', 'ibm', 'mas', 'ifa', 'mak', 'cmu', 'wat', 'add', 'pub', 'ner', 'rap', 'uci', 'hci', 'bad', 'act', 'dur', 'xml', 'ere', 'ith', 'mle', 'nso', 'rtf', 'rye', 'cen', 'pos', 'nis', 'dfi', 'sap', 'uti', 'min', 'dns', 'dic', 'ion', 'iin', 'val', 'gwe', 'tft', 'dft', 'rdb', 'ais', 'ddd', 'pso', 'knn', 'svm', 'nii', 'rel', 'jis', 'gap', 'vrt', 'ltu', 'dom', 'xof', 'bcr', 'atl', 'kas', 'iff', 'bim', 'rsv', 'vis', 'can', 'dth', 'Œªp', 'wto', 'emi', 'cis', 'cwe', 'prv', 'mar', '¬µj', 'fat', 'sur', 'xas', 'fas', 'dat', 'ova', 'nmi', 'cri', 'aic', 'mum', 'ceo', 'max', 'nbm', 'svd', 'dle', 'lsi', 'lda', 'tra', 'cpc', 'fin', 'rus', 'f b', 'tni', 'uat', 'vin', 'ata', 'aat', 'jeh', 'fox', 'cet', 'yue', 'psi', 'sec', 'enu', 'rbf', 'x n', 'ddt', 'fis', 'mhr', 'ses', 'wsj', 'rom', 'msc', 'flo', 'ore', 'pat', 'rdx', 'qas', 'xfs', 'esv', 'ied', 'isk', 'dtd', 'css', 'xsl', 'bmp', 'iso', 'vml', 'cgm', 'ino', 'nbe', 'fax', 'ocr', 'bis', 'iil', 'mdi', 'cla', 'dna', 'dfa', 'smp', 'sor', 'nav', 'nih', 'igm', 'chr', 'dls', 'gul', 'cbr', 'tty', 'iek', 'lto', 'irl', 'iwi', 'rtl', 'sal', 'yuc', 'pcp', 'aod', 'vhs', 'ltf', 'cea', 'htc', 'jtl', 'dis', 'raw', 'imh', 'f r', 'qbe', 'mbr', 'anf', 'sam', 'yil', 'dct', 'yis', 'rav', 'lue', 'dav', 'rgb', 'dwt', 'dsp', 'gnu', 'msn', 'cia', 'itt', 'lsc', 'hlr', 'rae', 'lwl', 'fir', 'faq', 'uol', 'wql', 'nlm', 'rts', 'nsf', 'hel', 'cpl', 'loc', 'neh', 'cda', 'eed', 'abe', 'ila', 's b', 'j r', 'iec', 'jli', 'jla', 'sil', 'dji', 'qki', 'mtm', 'kbe', 'atf', 'clu', 'cbe', 'ube', 'iss', 'ncr', 'apl', 'dnn', 'toy', 'upa', 'wmd', 'lce', 'sin', 'kim', 'gru', 'tai', 'lkl', 'mir', 'tct', 'txt', 'doc', '¬µt', 'xor', 'isbn', 'omar', ]
print(len(df))
df = df[~ df['concept'].isin(concepts_to_remove)]
print(df.columns)
print(len(df))
print(len(df))
df.to_csv("csv_concepts_wiki.tsv",sep="\t")

# df = pd.read_csv("csv_concepts_wiki.tsv",sep="\t")
# print(df['resource_id'].unique().head(20))