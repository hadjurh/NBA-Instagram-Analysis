# Clear environment
rm(list = ls())

# Load packages
require(magrittr)
require(lubridate)
require(ggplot2)
require(ggfortify)
require(plyr)
require(varhandle)
require(network)
require(sna)
require(GGally)

# Set working directory
# Project must be named "ttfl_planner" and be located in "~/Documents"'s sub-directory
dirname <- "database"
dirs <- list.dirs(path=file.path("~/Documents/"), recursive=T)
dir_wd <- names(unlist(sapply(dirs, grep, pattern=dirname))[1])
setwd(dir_wd)
rm(dirname,  dirs,  dir_wd)

# Get data
network <- read.csv2(file = 'frotteman/adjacency_matrix.csv',  sep = ',', header = FALSE)
user_data <- read.csv2(file = 'frotteman/player_username_id_team.csv', sep =',')
user_data <- user_data[-42,]
network <- network[-42,-42]
real_names <- user_data$NAME %>% unfactor()
usernames <- user_data$USERNAME %>% unfactor()
followers <- user_data$FOLLOWERS
nature <- user_data$NATURE %>% unfactor()

# Scale followers
min_scale <- 0.1
max_scale <- 10
followers = log(followers, 10)
min_fol <- followers %>% min()
max_fol <- followers %>% max()
followers = followers * ((max_scale - min_scale) / (max_fol - min_fol))
followers = (max_scale - followers %>% max()) + followers

# Set graph
net = network(network, 
              ignore.eval = TRUE, 
              names.eval = "weights")
network.vertex.names(net) = real_names
y = rainbow(21, s = 1, v = 1, start = 0, end = max(1, 21 - 1) / 21, alpha = 1)
y = substr(y,1,nchar(y)-2)
y = c("#FF0000", "#49FF00", "#FF00DB", "#FFDB00", "#DBFF00", "#0092FF",
  "#0049FF", "#00FF00", "#00FF49", "#4900FF", "#00FFDB", "#00DBFF",
  "#92FF00", "#FF0092", "#0000FF", "#00FF92", "#9200FF", "#DB00FF",
  "#FF9200", "#FF4900", "#FF0049")
names(y) = user_data$NATURE %>% levels()

# Plot
ggnet2(net, node.size = followers, node.color = nature,
       edge.size = 0.1, edge.color = "grey", 
       arrow.size = 7, arrow.gap = 0.01, 
       label = real_names, label.size = 6, label.color = 'black', palette = y) +
       guides(size=FALSE)

