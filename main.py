import utils_parser
# ----------------------------------------------------------------------------------------------------------------------
folder_in = './data/ex_logs/all/'
folder_out = './data/output/'
# ----------------------------------------------------------------------------------------------------------------------
filename_signatures = './data/signatures/signatures.txt'
filename_stopwords  = './data/signatures/stopwords.txt'
# ----------------------------------------------------------------------------------------------------------------------
P = utils_parser.Log_parser(folder_out,filename_signatures,filename_stopwords)
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    df_positions = P.search_signatures(folder_in)
    P.extract_fails(folder_in,df_positions)



