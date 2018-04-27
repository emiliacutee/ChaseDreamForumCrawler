# ChaseDreamForumCrawler
爬取cd论坛搜索页的信息～

https://forum.chasedream.com/search.php?mod=forum
chase dream论坛搜索页

注意，运行时输入的链接，需是点击搜索，再点击下面页码后出现的，结尾是page = n的链接（n为1位数字）

get_post_linksDates()
此函数用于获得搜索页各个帖子的链接及发帖时间

get_InterviewContent(urls)
此函数用于获得，点进各个帖子后，帖子的标题和内容

df_refine(df)
由于搜索页会出现许多被系统误判而我们并不需要的信息，这个函数用于优化搜索结果
你可以根据自己需要，自行修改过滤词，或不运行本函数

