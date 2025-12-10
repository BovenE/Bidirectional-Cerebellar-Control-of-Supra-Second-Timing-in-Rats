install.packages("lme4")
install.packages("lmerTest")
install.packages("MuMIn")
install.packages("ggplot2")
install.packages("jtools")
install.packages("broom")
install.packages("broom.mixed")
install.packages("ggstance")
install.packages("huxtable")
install.packages("performance")
install.packages("see")
install.packages("influence.ME")
install.packages("olsrr")
install.packages("sjPlot")
install.packages("sjlabelled")
install.packages("sjmisc")
install.packages("glmmTMB")
install.packages("multcomp")
install.packages("margins")
install.packages("ggeffects")
install.packages("car")

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
library(ggeffects)
library(car)

library(dplyr)
library(lme4)
library(lmerTest)
library(ggplot2)

library(dplyr)
library(lme4)
library(lmerTest)
library(ggplot2)

install.packages("dplyr")  # Install if not already installed
library(dplyr)  # Load dplyr before using summarise()

#path ='/Users/va18024/Library/CloudStorage/OneDrive-UniversityofBristol/Documents/PhD/Cerebellearning/Experimental/Analysis/EB_Analysis/R_scripts/GLM/ip3_dataset_NEWFINAL.csv'
path ='/Users/va18024/Library/CloudStorage/OneDrive-UniversityofBristol/Documents/PhD/Cerebellearning/Experimental/Analysis/EB_Analysis/R_scripts/GLM/ipREVIEW_combined_dataset_NEWFINAL.csv'


dframe <- read.csv(path)  



# Example: Suppose `df` contains a column `Trial_Index` representing trial occurrences
# and has columns: Rat, Group (Chemogenetic/Control), Drug (CNO/Vehicle), Trial_Index.

# Aggregate total number of trials per rat per condition
df_summary <- dframe %>%
  group_by(rat, group, manipulation, Session_date, stage) %>%
  summarise(TOT_Trials = n(), .groups = "drop")

df_summary$manipulation <- factor(df_summary$manipulation)

df_summary$manipulation <- relevel(df_summary$manipulation, ref = "VEH")


# Run a mixed-effects model (Random effect: Rat)
model_poisson <- glm(TOT_Trials ~ stage*group * manipulation,
                       data = df_summary, 
                       family = poisson)


summary(model_poisson)
anova(model_poisson)

conf_intervals <- confint(model_poisson, method = "profile")

# --- Summary ---
summary_df <- as.data.frame(coef(summary(model_poisson)))
write.csv(summary_df, "/Users/va18024/Library/CloudStorage/OneDrive-UniversityofBristol/Documents/PhD/Cerebellearning/Experimental/Analysis/EB_Analysis/R_scripts/GLM/output/Review/trials_summary.csv", row.names = TRUE)

# --- Confidence intervals ---
confint_df <- as.data.frame(confint(model_poisson, method = "Wald"))
write.csv(confint_df, "/Users/va18024/Library/CloudStorage/OneDrive-UniversityofBristol/Documents/PhD/Cerebellearning/Experimental/Analysis/EB_Analysis/R_scripts/GLM/output/Review/trials_Model1_confint.csv", row.names = TRUE)

# --- ANOVA table ---
anova_df <- as.data.frame(anova(model_poisson))
write.csv(anova_df, "/Users/va18024/Library/CloudStorage/OneDrive-UniversityofBristol/Documents/PhD/Cerebellearning/Experimental/Analysis/EB_Analysis/R_scripts/GLM/output/Review/trials_Model1_anova.csv", row.names = TRUE)


# Visualization (Optional)
ggplot(df_summary, aes(x = manipulation, y = TOT_Trials, fill = group)) +
  geom_boxplot() +
  theme_minimal() +
  labs(title = "Number of Trials by Group and Drug Condition")


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

# Additional custom formatting if necessary:
# For example, you can directly format output into a table with more structure

