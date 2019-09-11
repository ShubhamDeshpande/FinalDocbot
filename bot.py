from settings import ROOT_DIR
from scripts import brain as b

bot=b.Brain(ROOT_DIR)
while bot.percept.analysis.get('close') is None:
    query=input()
    temp=bot.predict(query)
    if temp[0]=="buffered_queries":
        buffered_ans=[]
        for query in temp[1]:
            buffered_ans.append(input(query))
        print(bot.process_buffered_queries(buffered_ans))
    else:
        print(temp[1])