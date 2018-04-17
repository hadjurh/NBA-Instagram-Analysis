# Clear environment
rm(list = ls())

# Load packages
require(magrittr)
require(lubridate)
require(ggplot2)
require(ggfortify)
require(plyr)
require(varhandle)
library(gridExtra)
library(grid)

# Set working directory
# Project must be named "ttfl_planner" and be located in "~/Documents"'s sub-directory
dirname <- "instagram_data"
dirs <- list.dirs(path=file.path("~/Documents/"), recursive=T)
dir_wd <- names(unlist(sapply(dirs,grep,pattern=dirname))[1])
setwd(dir_wd)
rm(dirname, dirs, dir_wd)

# Get data
kingjames <- read.csv2(file = '../NBA_Instagram_Analysis/database/instagram_user_by_user_data/kingjames/likes_comments.csv', sep = ',')
kingjames <- kingjames[, -1]
kingjames$DATE <- kingjames$DATE %>% strptime(format = '%Y-%m-%d %H:%M:%S', tz = 'EST')
kingjames$COLOR_OF_POINT <- ""
index_image <- kingjames$MEDIA == "Image"
index_video <- kingjames$MEDIA == "Video"
kingjames[index_image,]$COLOR_OF_POINT <- "blue"
kingjames[index_video,]$COLOR_OF_POINT <- "red"

# Remove outliers
# out = 0.07
# limits_likes <- quantile(kingjames$LIKE, probs = c(out, 1 - out))
# limits_comments <- quantile(kingjames$COMMENTS, probs = c(out, 1 - out))
# kingjames <- kingjames[kingjames$LIKE >= limits_likes[[1]] &
#                            kingjames$LIKE <= limits_likes[[2]],]
# kingjames <- kingjames[kingjames$COMMENTS >= limits_comments[[1]] &
#                            kingjames$COMMENTS <= limits_comments[[2]],]

# Plot
g <- ggplot(data = kingjames, aes(x = DATE %>% as_date(), 
                                  y = LIKES)) +
    geom_point(aes(colour = kingjames$MEDIA,
                   size = kingjames$COMMENTS),
               alpha = 0.8) + 
    ylab('Likes') +
    xlab('Date') + 
    guides(size = guide_legend(title ="Comments"),
           colour = guide_legend(title = 'Type of post')) + 
    scale_y_continuous(breaks = c(0, 500000, 1000000, 1500000, 2000000),
                       labels = c('0', '500,000', '1,000,000', '1,500,000', '2,000,000')) +
    scale_x_date(date_breaks = "1 year",
                 date_labels = "%Y-%m") +
    scale_size_continuous(breaks = c(min(kingjames$COMMENTS), 
                                     1e4, 5e4,
                                     1e5, 2.5e5, 
                                     max(kingjames$COMMENTS)),
                          labels = c(paste(formatC(min(kingjames$COMMENTS), format = "d", big.mark = ","), "(min)"), 
                                     "10,000", "50,000",
                                     "100,000", "250,000",
                                     paste(formatC(max(kingjames$COMMENTS), format = "d", big.mark = ","), "(max)")),
                          range = c(0.7, 6)) +
    scale_color_manual(values=c("dodgerblue", "red1")) +
    ggtitle("LeBron James (@KingJames) Instagram Feed in Numbers") + 
    theme(text = element_text(size = 15)) +
    labs(caption = "u/allstatsgame")
g
ggsave('../NBA_Instagram_Analysis/LeBron.png', width = 40, height = 16, units = 'cm')
