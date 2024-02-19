# Baidu_hc

1. get_url 从主页抓url
    - 写这个脚本的时候还只会selenium 
3. drp_baidu_hc.py  从信息页抓**问题、回答和副标题信息**
    - 到这里发现selenium实在太慢了 换了DrissonPage 30s变8s 官网在此 https://g1879.gitee.io/drissionpagedocs/history/statement 作者NB
    - 这里还有个小插曲，爬到第二页就有旋转图片的验证码了，一开始想死磕，用了这位老师的代码https://github.com/ShortCJL/RotateCode 和网盘里的模型，谢谢这位老师！实践下来还是有些太慢了，起码要花掉60s。后知后觉既然第二页有验证码，重启浏览器一直爬第一页不就行了😂
5. 问题分类.json  大致对问题进行分类总结
    - 分为一级分类和二级分类
7. baidu_hc_cls.py 生成给GPT的prompt，每条prompt包含问题分类.json中总结的给定范围
8. gpt3.5_annot.py  调GPT3.5给窝干活，这种简单的活就不劳烦GPT4啦
9. label_extract.py  代码判断提取
    - 简单过了一下输出，两个问题 ①多个tag输出 ②输出一些不在给定范围里的词 ③ 拿不准的时候就把全集都输出了
    - 代码逻辑：
        - 基于假设：问题一般不会太宽泛，即使命中多个二级分类，一般都不会跨越一级分类。
        - 逗号分割以后 过滤给定范围里的词，过滤后的词判断是不是所有词都是在同一个一级分类下面，是的就返回原字符串列表，否就返回空值待人工审核


相关的输入输出数据都在Data里
