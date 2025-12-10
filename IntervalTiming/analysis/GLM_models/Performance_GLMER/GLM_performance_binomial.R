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

path ='/Users/va18024/Library/CloudStorage/OneDrive-UniversityofBristol/Documents/PhD/Cerebellearning/Experimental/Analysis/EB_Analysis/R_scripts/GLM/ip3_dataset_NEWFINAL.csv'
#path ='/Users/va18024/Library/CloudStorage/OneDrive-UniversityofBristol/Documents/PhD/Cerebellearning/Experimental/Analysis/EB_Analysis/R_scripts/GLM/infusions3_dataset.csv'

dframe <- read.csv(path)  

my_data = dframe

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


dframe1["reward"][dframe1["reward"] == -1] <- 0

#Fixed effect models 
Model1 = glm(reward~1, family=binomial, data=dframe1)
Model2 = glm(reward~group, family=binomial, data=dframe1)

Model1 = glm(reward~group*manipulation, family=binomial, data=dframe1)
anova(Model1, test="Chisq")

((exp(coefficients(Model1)[1]+coefficients(Model1)[3])/(1+exp(coefficients(Model1)[1]+coefficients(Model1)[3])))-(exp(coefficients(Model1)[1])/(1+exp(coefficients(Model1)[1]))))*100
confint(Model1)

((exp(confint(Model1)[1]+confint(Model1)[3])/(1+exp(confint(Model1)[1]+confint(Model1)[3])))-(exp(confint(Model1)[1])/(1+exp(confint(Model1)[1]))))*100

((exp(confint(Model1)[1]+confint(Model1)[3+4])/(1+exp(confint(Model1)[1]+confint(Model1)[3+4])))-(exp(confint(Model1)[1])/(1+exp(confint(Model1)[1]))))*100


model_poisson = Model1

conf_intervals <- confint(model_poisson, method = "profile")


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



#Random intercept models 
Model5 = glmer(reward~group*manipulation +(1|Session_date)+(1|rat)+(1|trials_norm), family=binomial, data=dframe1)
Model6a = glmer(reward~group*manipulation +(1|rat)+(1|trials_norm), family=binomial, data=dframe1)
Model6 = glmer(reward~group*manipulation +(1|rat), family=binomial, data=dframe1)

Model7 = glmer(reward~group*manipulation +(1|trials_norm), family=binomial, data=dframe1)
Model8 = glmer(reward~group*manipulation +(1|Session_date), family=binomial, data=dframe1)


int=fixef(Model6)[1] 
coeff=fixef(Model6)[3] #get coefficient of manipulation
ranef(Model5)[3]
Anova(Model6, test="Chisq")

((exp(int+coeff)/(1+exp(int+coeff)))-(exp(int)/(1+exp(int))))*100
confint(Model6)

confint(Model5, maxpts = 8)

coeff1 <- -0.08830102
coeff2 <- 0.2550478
intc <- -0.24665844 
((exp(intc+coeff1)/(1+exp(intc+coeff1)))-(exp(intc)/(1+exp(intc))))*100

((exp(intc+coeff2)/(1+exp(intc+coeff2)))-(exp(intc)/(1+exp(intc))))*100






