#!/usr/local/bin/Rscript

#print(getwd())
datas= read.csv('../csv-and-graphs/anova/csv/done/cpu-delete.csv')
print(datas)
#n = rep(45, 4)
#print(n)
#group = rep(1:4, n)
#print(group)
#lm(BM ~ Docker, data=datas)
#lm(BM ~ DockerIso, data=datas)
#lm(BM ~ LXC, data=datas)
#lm(BM ~ Docker + DockerIso + LXC, data=datas)

print("NOW COMES ANOVA")
#fit <- aov(BM ~ Docker, data=datas)
#aov(BM ~ Error(Docker), data=datas)
#aov(BM ~ DockerIso, data=datas)
#aov(BM ~ LXC, data=datas)
fit <- aov(BM ~ Docker + DockerIso + LXC + Docker:DockerIso:LXC, data=datas)

plot(fit)