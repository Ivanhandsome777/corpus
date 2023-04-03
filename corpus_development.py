"""
仅作为日志使用，以下为语料库的搭建过程。包含了用到的所有模块以及函数。
如有改进可以先从这里看起
2023-4-3
"""

"""Env"""
import pandas as pd
import MeCab
import os
import glob
import requests
import re
from bs4 import BeautifulSoup
import bs4
import time
import zipfile
import unrar
import rarfile
import time
import datetime as dt
import warnings

warnings.filterwarnings("ignore")

"""Spider"""

def Gethtml(url, headers=None):
    try:
        re = requests.get(url, headers)
        re.raise_for_status()
        re.encoding = re.apparent_encoding
        html = re.text
        return html
    except:
        print('error')


def Parsehtml(html, list):
    soup = BeautifulSoup(html, 'html.parser')
    list.extend(soup.find_all('td', attrs={'colspan':'2'}))
    # list.extend(soup.find_all('td', attrs={'width': "182"}))
    # list.extend(soup.find_all('td', attrs={'width': "250"}))
    return list
  
  def spider_dialogue_html():
    raw_path = 'https://www.kitsunekko.net/'
    html = Gethtml('https://www.kitsunekko.net/dirlist.php?dir=subtitles%2Fjapanese%2F')
    list=[]
    list = Parsehtml(html, list)
    list_down_html = []
    for i in list:
        part1 = str(i).split("href=\"")[1].split("\"><strong>")[0]
        download_url = raw_path+part1
        list_down_html.append(download_url)
    return list_down_html

# list_down_html = spider_dialogue_html()
# print("动漫总数：",len(list_down_html))

# test_list = []
# for i in list_down_html:
#     lenth = len(i)
#     test_list.append(lenth)

def Parsehtml_step2(html, list):
    soup = BeautifulSoup(html, 'html.parser')
    list.extend(soup.find_all('td',attrs={"class":""}))
    # list.extend(soup.find_all('td', attrs={'width': "182"}))
    # list.extend(soup.find_all('td', attrs={'width': "250"}))
    return list
  
 
# html = Gethtml(list_down_html[1])
# list=[]
# list = Parsehtml_step2(html, list)
# raw_file_root=[]
# for url in list:
#     url_clean = str(url).split("href=\"")[1].split("\"><strong>")[0]
#     raw_file_root.append(url_clean)

"""
爬取一层url
"""
# def get_download_files_roots(list_down_html):
#     success_num = 0
#     raw_file_root=[]
#     lenth_all = len(list_down_html)
#     for i in range(lenth_all):
#         try:
#             html = Gethtml(list_down_html[i])
#             list=[]
#             list = Parsehtml_step2(html, list)
#             for url in list:
#                 url_clean = str(url).split("href=\"")[1].split("\"><strong>")[0]
#                 raw_file_root.append(url_clean)
#             success_num += 1
#             print("读取成功",success_num/lenth_all)
#             time.sleep(1)
#         except:
#             print("读取失败")
#             time.sleep(1)

#     return raw_file_root

# raw_file_root = get_download_files_roots(list_down_html)


"""
一层url已保存,可以直接读取
"""
file_name_step1 = '/Users/densoushin/Desktop/毕业论文/download_filename.txt'

# sep = '\n'
# with open(file_name_step1,'w') as f:
#     f.write(sep.join(raw_file_root))
# f.close()

with open(file_name_step1,'r') as f:
    content = f.read()
f.close()
raw_file_root = content.split("\n")

raw_file_root

# url = "https://www.kitsunekko.net/subtitles/japanese/7SEEDS/7SEEDS%20(01-12)%20(Webrip).zip"
# content = requests.get(url)
# with open('/Users/densoushin/Desktop/毕业论文/7SEEDS%20(01-12)%20(Webrip).zip','wb') as f:
#     f.write(content.content)
# f.close()
# zip_file = zipfile.ZipFile("/Users/densoushin/Desktop/毕业论文/7SEEDS%20(01-12)%20(Webrip).zip")
# zip_list = zip_file.namelist()
# for i in zip_list:
#     zip_file.extract(i,'/Users/densoushin/Desktop/毕业论文/')
# zip_file.close()


def get_origin_url(links):
    root_url = "https://www.kitsunekko.net/"
    cleaned_url_origin=[]
    for link in links:
        url = root_url+link
        url_cleaned = url.replace(" ",'%20')
        cleaned_url_origin.append(url_cleaned)
    return cleaned_url_origin
cleaned_url_origin =  get_origin_url(raw_file_root)

# url = 'https://www.kitsunekko.net/subtitles/japanese/3-gatsu%20no%20Lion/3月のライオン(1-22).rar'
# html = requests.get(url)
# with open("/Users/densoushin/Desktop/毕业论文/3月のライオン(1-22).rar",'wb') as f:
#     f.write(html.content)
# f.close()
# final_download_path = "/Users/densoushin/Desktop/毕业论文/11.rar"
# rar_file = rarfile.RarFile(final_download_path)

# final_download_path = root_document_url + file_name
# download_content = requests.get(url)
# with open(final_download_path,'wb') as f:
#     f.write(download_content.content)
# f.close()
# rar_file = rarfile.RarFile(final_download_path,mode='r')
# rf_list = rar_file.namelist()
# for f in rf_list:
#     rar_file.extract(f,root_document_url)
# rar_file.close()



"""
error_tip: 2023-2-12:
文件格式ass写错了,导致所有的ass格式文件没能下载成功
后续需要专门对ass格式的文件进行爬取
"""

def download_files2root(cleaned_url_origin):
    root_document = "/Users/densoushin/Desktop/毕业论文/"
    num=0
    lenth=len(cleaned_url_origin)
    error_file=[]
    for url in cleaned_url_origin:
        try:
            root_document_name = url.split("/")[-2]
            root_document_url = root_document + root_document_name + '/'
            file_type_name = os.path.splitext(url)[-1]
            file_name = url.split('/')[-1]
            if not os.path.exists(root_document_url):
                os.mkdir(root_document_url)
            if file_type_name in [".ssa",".srt",".ass"]:
                final_download_path = root_document_url + file_name
                download_content = Gethtml(url)
                with open(final_download_path,'w') as f:
                    f.write(download_content)
                f.close()
                

            elif file_type_name == '.rar':
                final_download_path = root_document_url + file_name
                download_content = requests.get(url)
                with open(final_download_path,'wb') as f:
                    f.write(download_content.content)
                f.close()
                rar_file = rarfile.RarFile(final_download_path,mode='r')
                rf_list = rar_file.namelist()
                for f in rf_list:
                    rar_file.extract(f,root_document_url)
                rar_file.close()
                
            else:
                final_download_path = root_document_url + file_name
                download_content = requests.get(url)
                with open(final_download_path,'wb') as f:
                    f.write(download_content.content)
                f.close()
                zip_file = zipfile.ZipFile(final_download_path)
                zip_list = zip_file.namelist()
                for f in zip_list:
                    zip_file.extract(f,root_document_url)
                zip_file.close()
            num+=1
            print("下载成功",final_download_path,'总数',num,'-',lenth)
            time.sleep(1)       
        except:
            error_file.append(url)
            print("输出失败")
    return error_file

error_file = download_files2root(cleaned_url_origin)


"""Extract Text"""

"""
这里可以用pysubs2模块
"""
from pysubs2 import SSAFile

def extract_text_from_file(subtitle_path,subtitle):    
    ssafile = SSAFile.load(subtitle_path)
    content=[]
    for text in ssafile:
        unit = text.plaintext
        # unit.remove('\n')
        content.append(unit)
    df = pd.DataFrame(content)
    df['anime'] = subtitle
    df.columns = ['subtitle_texts','anime']
    return df
 
root_path = '/Users/densoushin/Desktop/毕业论文/'
anime_list = os.listdir('/Users/densoushin/Desktop/毕业论文/')
anime_list.remove(".DS_Store")
anime_list.remove("download_filename.txt")
print(len(anime_list))

def transform_text2df(anime_list):
    error_list=[]
    df_list=[]
    for anime in anime_list:
        anime_path = root_path + anime + '/'
        subtitle_file_list = os.listdir(anime_path)
        for step,subtitle in enumerate(subtitle_file_list):
            subtitle_path = anime_path + subtitle
            file_type_name = os.path.splitext(subtitle)[-1]
            try:
                if file_type_name in ['.srt','.ass','.ssa']:
                    # Path = '/Users/densoushin/Desktop/subtitle_parquet/'+str(step)+'.parquet'
                    df = extract_text_from_file(subtitle_path,subtitle)
                    df_list.append(df)
                    # df.to_parquet(Path)
                    # print('输出成功:',Path)
                else:
                    pass
            except:
                print('输出失败',subtitle)
                error_list.append(subtitle)
    df_all = pd.concat(df_list)
    # now_timestamp = dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    
    return error_list, df_all
            
anime_list1 = anime_list[:500]
anime_list2 = anime_list[501:1000]
anime_list3 = anime_list[1001:1500]
anime_list4 = anime_list[1501:]
error_list, df_all = transform_text2df(anime_list4)
# error_list2 = transform_text2df(anime_list2)
# error_list3 = transform_text2df(anime_list3)
# error_list4 = transform_text2df(anime_list4)
with open("/Users/densoushin/Desktop/subtitle_parquet/error_list4.txt",'w') as f:
    f.writelines(error_list)
f.close()
df_all.to_parquet("/Users/densoushin/Desktop/subtitle_parquet/subtitle_sentence_4.parquet")


"""Split text"""

with open("/Users/densoushin/Desktop/subtitle_parquet/error_list1.txt",'w') as f:
    f.writelines(error_list1)
f.close()

df_1 = pd.read_parquet("./compiled_dataframe_2023-02-12-20-11-35.parquet")

def split_words(text_df):
    wakati = MeCab.Tagger("-Owakati") 
    shape_of_df = text_df.shape
    df_output_list = pd.DataFrame()
    for i in range(shape_of_df[0]):
        text,anime = text_df.iloc[i,]
        df = pd.DataFrame()
        splited_words = wakati.parse(text).split()
        df['word'] = splited_words
        df['subtitle_texts'] = text
        df['anime'] = anime
        df_output_list = df_output_list.append(df)
        # print(f'output {i} out of {shape_of_df[0]}')
    return df_output_list
  
  def partly_generate_parquet(df):
    n_row = math.floor(df.shape[0]/100)
    path_list = os.listdir("/Users/densoushin/Desktop/subtitle_parquet/subtitle_word_level_parquet1")
    path_list_names = [path.split('.')[0] for path in path_list]
    int_file_name_list = [int(x) for x in path_list_names]
    if int_file_name_list==[]:
        for j in range(99):
            df_unit = df.iloc[j*n_row:(j+1)*n_row]
            df_output_list_unit = split_words(df_unit)
            df_output_list_unit.to_parquet("/Users/densoushin/Desktop/subtitle_parquet/subtitle_word_level_parquet1/{}.parquet".format(j))
            print("output {} out of 100".format(j))
    else:
        continue_point = max(int_file_name_list)
        for j in range(99-continue_point-1):
            df_unit = df.iloc[(j+1+continue_point)*n_row:(j+2+continue_point)*n_row]
            df_output_list_unit = split_words(df_unit)
            df_output_list_unit.to_parquet("/Users/densoushin/Desktop/subtitle_parquet/subtitle_word_level_parquet1/{}.parquet".format(j+1+continue_point))
            print("output {} out of 100".format(j+1+continue_point))
    return 0

status = partly_generate_parquet(df_1)


"""calculate the information"""
