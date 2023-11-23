import os
import re
import pandas as pd
import numpy
import tools_IO
import tools_DF
# ----------------------------------------------------------------------------------------------------------------------
class Log_parser():

    def __init__(self, folder_out, filename_signatures, filename_stopwords):
        self.folder_out = folder_out
        self.signatures = self.init_signatures(filename_signatures)
        self.stopwords = self.init_stopwords(filename_stopwords)
        return
# ----------------------------------------------------------------------------------------------------------------------
    def init_signatures(self,filename_signatures):
        with open(filename_signatures,'r') as f:
            signatures = [s.strip() for s in f.readlines()]
        return signatures
# ----------------------------------------------------------------------------------------------------------------------
    def init_stopwords(self,filename_stopwords):
        with open(filename_stopwords, 'r') as f:
            stopwords = [s.strip() for s in f.readlines()]
        return stopwords
# ----------------------------------------------------------------------------------------------------------------------
    def search_signatures(self,folder_in):
        res = []
        filenames = tools_IO.get_filenames(folder_in,'*.*')
        for filename in filenames:
            with open(folder_in+filename,'r') as f:
                lines = f.readlines()
                ss = [i for i,l in enumerate(lines) for s in self.signatures if s in l]
                res.append([filename,min(ss) if len(ss)>0 else numpy.nan]),

        df_positions = pd.DataFrame(res,columns=['filename','pos'])
        return df_positions
# ----------------------------------------------------------------------------------------------------------------------
    def derive_failed_targets(self, text_message):
        file_path_pattern = r"/[\w/.-]+"
        file_paths = re.findall(file_path_pattern, text_message)
        file_paths = set([f for f in file_paths if f not in self.stopwords])
        return '\n'.join(file_paths)
# ----------------------------------------------------------------------------------------------------------------------
    def extract_fails(self,folder_in, df_positions):
        tools_IO.remove_files(self.folder_out,'*.*')
        df_positions['failed_targets'] = ''

        for r in range(df_positions.shape[0]):
            pos = df_positions.iloc[r, 1]
            filename = df_positions.iloc[r,0]
            if not os.path.isfile(folder_in+filename):
                continue

            with open(folder_in+filename,'r') as f:
                lines_fail = f.readlines()[pos:pos + 10]
                failed_targets = self.derive_failed_targets('\n'.join(lines_fail))

            df_positions.iloc[r,-1] = failed_targets

            with open(self.folder_out+filename,'w') as g:
                g.write(failed_targets)
                g.write('\n')
                g.write(''.join(['-']*80))
                g.write('\n')
                g.writelines(lines_fail)

        print(tools_DF.prettify(df_positions))
        return
# ----------------------------------------------------------------------------------------------------------------------