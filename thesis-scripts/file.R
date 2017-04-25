#!/usr/local/bin/Rscript

#print(getwd())
#datas= read.csv('../csv-and-graphs/anova/csv/done/cpu-update.csv')
datas= read.csv('../csv-and-graphs/anova/comp-csv/done/sent-read.csv')
#print(datas)
stf <- stack(datas)
names(stf) <- c("metric", "architecture")
#print(stf)
res <- aov(metric ~ architecture, data=stf)
summary(res)
tk <- TukeyHSD(res)
print(tk)
#plot(res)
