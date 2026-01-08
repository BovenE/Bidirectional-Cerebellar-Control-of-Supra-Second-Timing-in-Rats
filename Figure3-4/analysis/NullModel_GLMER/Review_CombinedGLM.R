library(dplyr)


path ='/Users/va18024/Library/CloudStorage/OneDrive-UniversityofBristol/Documents/PhD/Cerebellearning/Experimental/Analysis/EB_Analysis/R_scripts/GLM/ipREVIEW_combined_dataset_NEWFINAL.csv'

dframe <- read.csv(path)  

#reduce dataset to have normal distribution (closer)
dframe_sub <- subset(dframe, reward>-1 & t_hold<=(450/100) & t_hold>(20/100))#& group=='C')# & trial==1)# & rat != 'TITET_19'& rat != 'TITET_20') #& trial==1) %
my_data = dframe_sub

dframe1=my_data
dframe1$group <- as.factor(dframe1$group)
dframe1$manipulation <- as.factor(dframe1$manipulation)
dframe1$manipulation <- factor(dframe1$manipulation, levels = levels(dframe1$manipulation)[2:1])
#dframe1$sensory_state <- as.factor(dframe1$sensory_state)
dframe1$trial <- as.factor(dframe1$trial)
dframe1$Session_date=as.character(dframe1$Session_date)
dframe1$Session_date <- as.Date(dframe1$Session_date, '%Y%m%d')
#dframe1$reward <- as.factor(dframe1$reward)
dframe1$rat <- as.factor(dframe1$rat)
dframe1$stage <- as.factor(dframe1$stage)

#dframe1$stage <- factor(dframe1$stage, levels = levels(dframe1$stage)[2:1])

Model5 = lmer(t_hold~stage*manipulation*group+(1|Session_date)+(1|rat), data=dframe1,REML = TRUE)#
summary(Model5)
confint(Model5)
anova(Model5)

# --- Summary ---
summary_df <- as.data.frame(coef(summary(Model5)))
write.csv(summary_df, "/Users/va18024/Library/CloudStorage/OneDrive-UniversityofBristol/Documents/PhD/Cerebellearning/Experimental/Analysis/EB_Analysis/R_scripts/GLM/output/Review/t_hold_summary.csv", row.names = TRUE)

# --- Confidence intervals ---
confint_df <- as.data.frame(confint(Model5, method = "Wald"))
write.csv(confint_df, "/Users/va18024/Library/CloudStorage/OneDrive-UniversityofBristol/Documents/PhD/Cerebellearning/Experimental/Analysis/EB_Analysis/R_scripts/GLM/output/Review/t_hold_Model5_confint.csv", row.names = TRUE)

# --- ANOVA table ---
anova_df <- as.data.frame(anova(Model5))
write.csv(anova_df, "/Users/va18024/Library/CloudStorage/OneDrive-UniversityofBristol/Documents/PhD/Cerebellearning/Experimental/Analysis/EB_Analysis/R_scripts/GLM/output/Review/t_hold_Model5_anova.csv", row.names = TRUE)

library(emmeans)
emmeans(Model5, ~ stage * manipulation * group)
hist(resid(Model5_log), breaks=50)


interaction.plot(x.factor = my_data$stage, trace.factor = my_data$manipulation, 
                 response = my_data$t_hold , fun = mean, 
                 type = "b", legend = TRUE, 
                 xlab = "group", ylab="Exit time (cs)",
                 pch=c(1,19))


avg_df <- dframe1 %>%
  group_by(group, rat, manipulation) %>%
  summarise(mean_value = mean(t_hold, na.rm = TRUE), .groups = 'drop')
