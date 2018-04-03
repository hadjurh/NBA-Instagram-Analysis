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
real_names <- user_data$NAME %>% unfactor()
usernames <- user_data$USERNAME %>% unfactor()
followers <- user_data$FOLLOWERS

# Scale followers
min_scale <- 2
max_scale <- 20
min_fol <- followers %>% min()
max_fol <- followers %>% max()
followers = followers * ((max_scale - min_scale) / (max_fol - min_fol))
followers = (max_scale - followers %>% max()) + followers

# Set graph
net = network(network, 
              ignore.eval = TRUE, 
              names.eval = "weights")
network.vertex.names(net) = usernames

# Plot
ggnet2(net, node.size = followers,
       edge.size = 0.1, edge.color = "grey", 
       arrow.size = 4, arrow.gap = 0.005, 
       label = usernames, label.size = 5, label.color = 'grey28') + 
    theme(legend.position = "none")
