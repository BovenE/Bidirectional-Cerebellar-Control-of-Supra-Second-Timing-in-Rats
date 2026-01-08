#these packages must be called before working through script (each time r is opened)
library(lme4)
library(lmerTest)
library(MuMIn)
library (ggplot2)
library (jtools)
library (broom)
library (broom.mixed)
library (ggstance)
library (huxtable)
library (performance)
library (see)
library(influence.ME)
library (olsrr)
library (sjPlot)
library (sjlabelled)
library(sjmisc)
library (glmmTMB)
library(multcomp)
library(margins)
#library(ggpubr)

#load data
path ='/Users/va18024/Library/CloudStorage/OneDrive-UniversityofBristol/Documents/PhD/Cerebellearning/Experimental/Analysis/EB_Analysis/R_scripts/GLM/ip3_dataset_NEWFINAL.csv'
#path ='/Users/va18024/Library/CloudStorage/OneDrive-UniversityofBristol/Documents/PhD/Cerebellearning/Experimental/Analysis/EB_Analysis/R_scripts/GLM/infusions3_dataset.csv'

dframe <- read.csv(path)  

#reduce dataset
#dframe_sub <- subset(dframe, t_hold<=(350) & t_hold>(20) & reward>-1)
dframe_sub <- subset(dframe, reward_lat>0)
my_data = dframe_sub


dframe1=my_data
dframe1$group <- as.factor(dframe1$group)
dframe1$manipulation <- as.factor(dframe1$manipulation)
dframe1$manipulation <- factor(dframe1$manipulation, levels = levels(dframe1$manipulation)[2:1])
dframe1$sensory_state <- as.factor(dframe1$sensory_state)
#dframe1$trial <- as.factor(dframe1$trial)
dframe1$Session_date=as.character(dframe1$Session_date)
dframe1$Session_date <- as.Date(dframe1$Session_date, '%Y%m%d')
#dframe1$reward <- as.factor(dframe1$reward)
dframe1$rat <- as.factor(dframe1$rat)






Model1 = lmer(reward_lat~group*manipulation+(1|Session_date)+(1|rat), data=dframe1)
summary(Model1)
confint(Model1)
anova(Model1)
ggpredict(Model1, c("group", "manipulation"))%>% plot()

conf_intervals <- confint(model_poisson, method = "profile")

model_poisson = Model1
# Capture the summary output
model_summary <- capture.output(summary(model_poisson))

# Optional: Save the model summary to a text file (Basic Output)
writeLines(model_summary, "model_summary.txt")

# For a more detailed output (like confidence intervals, p-values):
# Capture the confidence intervals for the fixed effects
conf_intervals <- capture.output(confint(model_poisson, method = "profile"))

# Combine the output (model summary + confidence intervals) into one object
full_output <- c(model_summary, "Confidence Intervals:", conf_intervals)

# Write the full output to a text file
writeLines(full_output, "detailed_model_summary.txt")

# If you want to capture ANOVA results for the model
anova_results <- capture.output(anova(model_poisson))
writeLines(anova_results, "anova_results.txt")




qqnorm(dframe1$t_hold)
abline(0,1)

ggpredict(Model1, "group")


qqnorm(resid(Model5))
abline(0,1, col = "red", lty = 2)

