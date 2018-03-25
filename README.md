# pyltp-plot
基于matplotlib画出pyltp结果

由于每次在ltp官网上进行某个句子的测试有点麻烦。加入自己的词典也不方便。

所以写了个小工具，直接画出pyltp分析的结果。

代码很简单，传入四个参数：words, postags, nes, deps即可。
其中words是分词结果，postags是词性标注结果，nes是命名实体分析结果，deps是依存关系结果。

nes渲染还没做，先这么用着。
