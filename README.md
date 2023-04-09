# corpus-日语动漫口语语料库
语料库预料来源于网络，包含了30年来2600多部主流动漫；题材涵盖热血、恋爱、校园、城市、生活等，十分全面。同时，动漫的对话特征也决定了其与口语的紧密联系。  
接下来详细介绍语料库的构建：  
三个文件中Ivan_corpus_v1.py是脚本文件

## 使用方法
### step1:下载语料库  
link：https://drive.google.com/file/d/1w4vmt2Fb9gyeD9k9gwWQc8hAIoFOBMwm/view?usp=share_link  
下载完成此文件后，将此文件与 Ivan_corpus_v1.py 放到同一个目录下  
  
### step2:加载语料库
运行Ivan_corpus_v1.py文件，加载语料库对象  
创建语料库对象 `corpus_new = IvanCorpus()`  

### step3:语料库函数
单词查询 `corpus_new.search_word(word_search,digit)`.  
其中，word_search是需要查询的单词，digit是输出参数的小数点位数。
  

批量查询 `corpus_new.batch_search(words_list,digit,export_to_excel=False,export_path="./",export_file_name='output1.xlsx')`  
其中words_list是查询单词列表，digit是输出参数小数位数。  
export_to_excel表示是否输出为xlsx文件。  
export_path表示输出文件路径，export_file_name表示输出文件名称。  


## 更新方向
1、模块化；2、自动下载语料库资源；3、功能优化；4、速度提升
