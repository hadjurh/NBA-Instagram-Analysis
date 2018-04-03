# Clear environment
rm(list = ls())

# Load packages
require(magrittr)
require(lubridate)
require(ggplot2)
require(ggfortify)
require(plyr)
require(varhandle)

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

# Remove outliers
out = 0.07
limits_likes <- quantile(kingjames$LIKE, probs = c(out, 1 - out))
limits_comments <- quantile(kingjames$COMMENTS, probs = c(out, 1 - out))
kingjames <- kingjames[kingjames$LIKE >= limits_likes[[1]] &
                           kingjames$LIKE <= limits_likes[[2]],]
kingjames <- kingjames[kingjames$COMMENTS >= limits_comments[[1]] &
                           kingjames$COMMENTS <= limits_comments[[2]],]

# Plot
g <- ggplot(data = kingjames, aes(x = DATE %>% as_date(), 
                                  y = LIKE)) +
    geom_point(aes(colour=kingjames$MEDIA,
                   size=kingjames$COMMENTS)) + 
    scale_x_date(date_labels = "%Y-%m") + 
    scale_size_continuous(range = c(1,3))
g

