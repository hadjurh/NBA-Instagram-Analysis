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
require(colorRamps)

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
max_scale <- 5
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
nature_length = user_data$NATURE %>% levels() %>% length()
y = rainbow(nature_length, 
            s = 1, v = 1, start = 0, 
            end = max(1, nature_length - 1) / nature_length, 
            alpha = 1)
y = substr(y,1,nchar(y)-2)
y = c(
 "red3","red","orange3",
 "orange","orchid",
 "magenta","slateblue1",
 "steelblue1","#00FFFF",
 "dodgerblue2", "olivedrab1",
 "lawngreen","forestgreen",
 "yellow1","gold1",
 "darkorchid2","#FF0055", "#AAAAAA")
names(y) = user_data$NATURE %>% levels()

# Plot
ggnet2(net, node.size = followers, node.color = nature,
       edge.size = 0.3, edge.color = "grey", 
       arrow.size = 3, arrow.gap = 0.01, 
       label = real_names, label.size = 3, label.color = 'black', palette = y) +
       guides(size=FALSE)

