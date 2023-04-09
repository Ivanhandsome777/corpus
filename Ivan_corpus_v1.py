import pandas as pd
import numpy as np
import math


class IvanCorpus:
    corpus_content_default = pd.read_parquet("/Users/densoushin/Desktop/上财大四下/Japanese_anime_corpus/version1_corpus.parquet")
    def __init__(self,corpus_content=corpus_content_default):
        self.corpus_content = corpus_content
        self.shape = corpus_content.shape
        self.version='0.1.0'
        self.anime_scale = len(corpus_content.anime.unique())
        self.words_num = corpus_content.shape[0]
        self.corpus_frequency = corpus_content.groupby(['word'],as_index=0).agg({'subtitle_texts':'count','anime':'nunique'}).rename(columns={'subtitle_texts':'word_frequency','anime':'n_anime'})
    
    
    def search_word(self,word_search,digit=2,root_sentence=False,root_anime=False):
        df = self.corpus_content
        df_word_frequency = self.corpus_frequency
        anime_scale = self.anime_scale
        word_scale = self.words_num
        CHR_count = int(df_word_frequency.query("""word ==@word_search""")['word_frequency'])
        CHR_million = np.round(CHR_count/(word_scale/1000000),digit)
        log_CHR = np.round(math.log10(CHR_count),digit)
        CHR_CD = int(df_word_frequency.query("""word ==@word_search""").n_anime)
        CHR_CD_per = np.round(CHR_CD/anime_scale,digit)
        log_CHR_CD = np.round(math.log10(CHR_CD),digit)
        print("word:",word_search,"\n","CHR_count:",CHR_count,"\n","CHR_million:",CHR_million,"\n","log_CHR:",log_CHR,"\n","CHR_CD:",CHR_CD,"\n","CHR_CD_per:",CHR_CD_per,"\n","log_CHR_CD:",log_CHR_CD,"\n")

    def batch_search(self,words_list,digit=2,export_to_excel=False,export_path="./",export_file_name='output1.xlsx',root_sentence=False,root_anime=False):
        df = self.corpus_content
        df_word_frequency = self.corpus_frequency
        anime_scale = self.anime_scale
        word_scale = self.words_num
        list_df=[]
        for word in words_list:
            try:
                CHR_count = int(df_word_frequency.query("""word ==@word""")['word_frequency'])
                CHR_million = np.round(CHR_count/(word_scale/1000000),digit)
                log_CHR = np.round(math.log10(CHR_count),digit)
                CHR_CD = int(df_word_frequency.query("""word ==@word""").n_anime)
                CHR_CD_per = np.round(CHR_CD/anime_scale,digit)
                log_CHR_CD = np.round(math.log10(CHR_CD),digit)
                dict_value = {
                    "word":word,
                    "CHR_count":CHR_count,
                    "CHR_million":CHR_million,
                    "log_CHR":log_CHR,
                    "CHR_CD":CHR_CD,
                    "CHR_CD_per":CHR_CD_per,
                    "log_CHR_CD":log_CHR_CD
                }
                df_unit = pd.DataFrame(dict_value,index=[0])
                list_df.append(df_unit)
            except:
                print(word,"is not in the corpus")
        out_put_df = pd.concat(list_df)
        if export_to_excel is True:
            out_put_df.to_excel(export_path+export_file_name)
            print("successfully export",export_path,export_file_name)
        else:
            return out_put_df
    
    

    
    
