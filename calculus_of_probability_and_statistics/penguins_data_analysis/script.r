# needed packages
library(psych)
library(ggplot2)
library(magrittr)
library(dplyr)
library(ggpubr)
library(reshape2)
library(ggcorrplot)
library(stats)


# needed data
install.packages("palmerpenguins", 
                 repos = "https://cloud.r-project.org/")
library(palmerpenguins)
data(package = 'palmerpenguins')
penguins_data <- penguins

# alternative way to obtain data
#penguins_data <- read.csv(file = "penguins.csv", 
#                          header = TRUE, 
#                          stringsAsFactors = TRUE)

# data cleaning
penguins_data <- na.omit(penguins_data)
penguins_data$year <- as.factor(penguins_data$year)

# show data example
str(penguins_data)

# mean, quartiles, median, standard deviation
summary(penguins_data)

# more informations for numeric values, like kurtosis, skew
describeBy(penguins_data[c(3:6)])

# first boxplot of numeric values
melted <- melt(penguins_data[c(3:6)])
ggplot(melted, aes(x=variable, y=value, 
                   fill=variable)) +
  geom_boxplot(alpha=0.8) +
  facet_wrap(~variable, scales="free", ncol=4, nrow=1) +
  scale_fill_manual(values = c("#22577A","#38A3A5","#57CC99", "#80ED99"), 
                    guide = "none") +
  theme_minimal() +
  theme(
    legend.position="none",
    text=element_text(family='mono', face="bold"),
    title=element_text(size=15, family='mono', face="bold"),
    axis.text.y=element_text(size=12, family='mono', face="bold"),
    axis.text.x=element_blank(),
    axis.title=element_blank(), 
  )

# densiti plots for numeric values
style <- theme_minimal() +
  theme(
    legend.position="none",
    text=element_text(family='mono', face="bold"),
    title=element_text(size=12, family='mono', face="bold"),
    axis.text=element_text(size=12, family='mono', face="bold"),
    axis.title.y=element_blank()
  )

fg1 <- ggplot(penguins_data, aes(x=bill_length_mm)) + geom_density(fill="#22577A", color="#e9ecef", alpha=0.8) + style
fg2 <- ggplot(penguins_data, aes(x=bill_depth_mm)) + geom_density(fill="#38A3A5", color="#e9ecef", alpha=0.8) + style
fg3 <- ggplot(penguins_data, aes(x=flipper_length_mm)) + geom_density(fill="#57CC99", color="#e9ecef", alpha=0.8) + style
fg4 <- ggplot(penguins_data, aes(x=body_mass_g)) + geom_density(fill="#69b3a2", color="#e9ecef", alpha=0.8) + style

ggarrange(fg1, fg2, fg3, fg4,
          ncol=2, nrow=2, font.label=list(size = 12, family='mono'))

# species vs island of observation (count) and plot
penguins_data %>% count(species, island)

ggplot(penguins_data, aes(x = island, fill = species)) +
  geom_bar(alpha = 0.8) +
  scale_fill_manual(values = c("#22577A","#38A3A5","#57CC99"),
                    guide = "none") +
  theme_minimal() +
  facet_wrap(~species, ncol = 1) +
  coord_flip() +
  theme(text=element_text(family='mono', face="bold"),
        title=element_text(family='mono', face="bold"),
        axis.text=element_text(size=15, family='mono', face="bold"), 
        axis.title=element_text(size=18, family='mono', face="bold"))

# species vs sex (count) and plot
penguins_data %>% count(sex, species)

ggplot(penguins_data, aes(x = sex, fill = species)) +
  geom_bar(alpha = 0.8) +
  scale_fill_manual(values = c("#22577A","#38A3A5","#57CC99"),
                    guide = "none") +
  theme_minimal() +
  facet_wrap(~species, ncol = 1) +
  coord_flip() +
  theme(text=element_text(family='mono', face="bold"),
        title=element_text(family='mono', face="bold"),
        axis.text=element_text(size=15, family='mono', face="bold"), 
        axis.title=element_text(size=18, family='mono', face="bold"))

# means grouped by species fro all numeric value and plot
penguins_data %>% group_by(species) %>% 
  summarise(across(-c(island, sex, year), mean))

style <- theme_minimal() +
  theme(
    legend.position="none",
    text=element_text(family='mono', face="bold"),
    title=element_text(size=12, family='mono', face="bold"),
    axis.text=element_text(size=10, family='mono', face="bold"),
    axis.title.x=element_blank(),
  )

gb1 <- ggplot(penguins_data, aes(x = species, y = bill_length_mm)) + 
  geom_bar(stat = "summary", fun = "mean", fill="#22577A", color="#e9ecef", alpha=0.8) + style
gb2 <- ggplot(penguins_data, aes(x = species, y = bill_depth_mm)) + 
  geom_bar(stat = "summary", fun = "mean", fill="#38A3A5", color="#e9ecef", alpha=0.8) + style
gb3 <- ggplot(penguins_data, aes(x = species, y = flipper_length_mm)) + 
  geom_bar(stat = "summary", fun = "mean", fill="#57CC99", color="#e9ecef", alpha=0.8) + style
gb4 <- ggplot(penguins_data, aes(x = species, y = body_mass_g)) + 
  geom_bar(stat = "summary", fun = "mean", fill="#69b3a2", color="#e9ecef", alpha=0.8) + style

ggarrange(gb1, gb2, gb3, gb4,
          ncol=2, nrow=2, font.label=list(size = 12, family='mono'))

# means grouped by species and sex, but w/o plot
penguins_data %>% group_by(species, sex) %>% 
  summarise(across(-c(island, year), mean))

# correlation matrix
corr <- round(cor(penguins_data[c(3:6)]), 2)

ggcorrplot(corr, 
           ggtheme=ggplot2::theme_minimal,
           colors=c("#22577A", "white", "#38A3A5"),
           lab=TRUE) +
  theme(
    text=element_text(family='mono', face="bold"),
    title=element_text(size=12, family='mono', face="bold"),
    axis.text=element_text(size=10, family='mono', face="bold")
  )

# plot for flipper_length_mm and body_mass_g
ggplot(penguins_data, aes(x = flipper_length_mm, y = body_mass_g)) +
  geom_point(aes(color = species,
                 shape = species),
             size = 2) +
  scale_color_manual(values = c("#22577A","#38A3A5","#57CC99", "#80ED99")) +
  theme_minimal() +
  theme(
    text=element_text(family='mono', face="bold"),
    title=element_text(size=12, family='mono', face="bold"),
    axis.text=element_text(size=10, family='mono', face="bold"),
  )

# plot for bill_length_mm and bill_depth_mm (with species highlited)
ggplot(penguins_data, aes(x = bill_length_mm, y = bill_depth_mm)) +
  geom_point(aes(color = species,
                 shape = species),
             size = 2) +
  scale_color_manual(values = c("#22577A","#38A3A5","#57CC99", "#80ED99")) +
  theme_minimal() +
  theme(
    text=element_text(family='mono', face="bold"),
    title=element_text(size=12, family='mono', face="bold"),
    axis.text=element_text(size=10, family='mono', face="bold"),
  )

# histogram for body_mass_g
ggplot(penguins_data, aes(x=body_mass_g)) + 
  geom_histogram(color = "#38A3A5", fill = "#38A3A5", alpha = 0.8)+
  theme_minimal() + 
  theme(
    text=element_text(family='mono', face="bold"),
    title=element_text(size=12, family='mono', face="bold"),
    axis.text=element_text(size=10, family='mono', face="bold"),
  )

# Q-Q plot for body_mass_g
ggplot(penguins_data, aes(sample = body_mass_g)) +
  stat_qq(color = "#22577A") +
  stat_qq_line(color = "#38A3A5") +
  theme_minimal() +
  theme(
    legend.position="none",
    text=element_text(family='mono', face="bold"),
    title=element_text(size=12, family='mono', face="bold"),
    axis.title=element_blank(),
  )

# Shapiro-Wilk test
shapiro.test(sample(penguins_data$body_mass_g, 50))

# function for mean confidence interval for body_mass_g
meanCI <- function(x, conf.level) {
  alpha <- 1 - conf.level
  n <- length(x)
  return (c(mean(x) - qt(1-alpha/2, n-1)*sd(x)/ sqrt(n),
            mean(x) + qt(1-alpha/2, n-1)*sd(x)/ sqrt(n))
  )
}
meanCI(penguins_data$body_mass_g, 0.95)

# the same function as above, but from stats package
t.test(penguins_data$body_mass_g)$"conf.int"

