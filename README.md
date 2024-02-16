# Baidu_hc

1. get_url 从主页抓url #写这个脚本的时候还只会selenium 
2. drp_baidu_hc.py  从信息页抓**问题、回答和副标题信息** #到这里发现selenium实在太慢了 换了DrissonPage 30s变8s 官网在此 https://g1879.gitee.io/drissionpagedocs/history/statement 作者NB
  - 这里还有个小插曲，爬到第二页就有旋转图片的验证码了，一开始想死磕，用了这位老师的代码https://github.com/ShortCJL/RotateCode 和网盘里的模型，谢谢这位老师！实践下来还是有些太慢了，起码要花掉60s。后知后觉既然第二页有验证码，重启浏览器一直爬第一页不就行了😂
4. 问题分类.json  大致对问题进行分类总结
5. baidu_hc_cls.py 生成给GPT的prompt
6. gpt3.5_annot.py  调GPT3.5给窝干活
7. label_extract.py  代码判断提取


相关的输入输出数据都在Data里
