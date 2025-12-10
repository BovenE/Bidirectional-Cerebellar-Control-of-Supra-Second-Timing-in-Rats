library(dplyr)


path ='/Users/va18024/Library/CloudStorage/OneDrive-UniversityofBristol/Documents/PhD/Cerebellearning/Experimental/Analysis/EB_Analysis/R_scripts/GLM/ipREVIEW_combined_dataset_NEWFINAL.csv'

dframe <- read.csv(path)  

#reduce dataset
#dframe_sub <- subset(dframe, t_hold<=(350) & t_hold>(20) & reward>-1)
my_data = dframe


dframe1=my_data
dframe1$group <- as.factor(dframe1$group)
dframe1$manipulation <- as.factor(dframe1$manipulation)
dframe1$manipulation <- factor(dframe1$manipulation, levels = levels(dframe1$manipulation)[2:1])
#dframe1$sensory_state <- as.factor(dframe1$sensory_state)
#dframe1$trial <- as.factor(dframe1$trial)
dframe1$Session_date=as.character(dframe1$Session_date)
dframe1$Session_date <- as.Date(dframe1$Session_date, '%Y%m%d')
#dframe1$reward <- as.factor(dframe1$reward)
dframe1$rat <- as.factor(dframe1$rat)
dframe1$stage <- as.factor(dframe1$stage)


dframe1["reward"][dframe1["reward"] == -1] <- 0


Model1 = glm(reward~1, family=binomial, data=dframe1)
Model2 = glm(reward~group, family=binomial, data=dframe1)
Model3 = glm(reward~group+manipulation, family=binomial, data=dframe1)
Model4 = glm(reward~stage*manipulation, family=binomial, data=dframe1)

Model1 = glm(reward~stage*manipulation*group, family=binomial, data=dframe1)
anova(Model1, test="Chisq")
summary(Model1)

# --- Summary ---
summary_df <- as.data.frame(coef(summary(Model1)))
write.csv(summary_df, "/Users/va18024/Library/CloudStorage/OneDrive-UniversityofBristol/Documents/PhD/Cerebellearning/Experimental/Analysis/EB_Analysis/R_scripts/GLM/output/Review/performance_summary.csv", row.names = TRUE)

# --- Confidence intervals ---
confint_df <- as.data.frame(confint(Model1, method = "Wald"))
write.csv(confint_df, "/Users/va18024/Library/CloudStorage/OneDrive-UniversityofBristol/Documents/PhD/Cerebellearning/Experimental/Analysis/EB_Analysis/R_scripts/GLM/output/Review/performance_Model5_confint.csv", row.names = TRUE)

# --- ANOVA table ---
anova_df <- as.data.frame(anova(Model1))
write.csv(anova_df, "/Users/va18024/Library/CloudStorage/OneDrive-UniversityofBristol/Documents/PhD/Cerebellearning/Experimental/Analysis/EB_Analysis/R_scripts/GLM/output/Review/performance_Model5_anova.csv", row.names = TRUE)


ggpredict(Model1, c("group", "manipulation"))%>% plot()



qqnorm(dframe1$t_hold)
abline(0,1)

ggpredict(Model1, "group")


qqnorm(resid(Model5))
abline(0,1, col = "red", lty = 2)
