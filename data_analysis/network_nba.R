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
network <- read.csv2(file = 'network_players_gt46_games/adjacency_matrix.csv',  sep = ',', header = FALSE)
player_data <- read.csv2(file = 'network_players_gt46_games/player_username_id_team.csv', sep =',')
player_names <- player_data$NAME %>% unfactor()
usernames <- player_data$USERNAME %>% unfactor()
followers <- player_data$FOLLOWERS
teams <- player_data$TEAM %>% unfactor()
colors <- read.csv2(file = '../../ttfl_planner/r_data_analysis/team_colors.csv', sep = ',')

# Scale followers
min_scale <- 2
max_scale <- 20
followers <- log(followers, base = 10)
min_fol <- followers %>% min()
max_fol <- followers %>% max()
followers = followers * ((max_scale - min_scale) / (max_fol - min_fol))
followers = (max_scale - followers %>% max()) + followers
    
# Set graph
net = network(network, 
              ignore.eval = TRUE, 
              names.eval = "weights")
net %v% "team" = as.character(teams)
network.vertex.names(net) = usernames
y = colors$COLOR %>% as.vector()
names(y) = c('CLE', 'BOS', 'HOU', 'GSW', 'DET', 'CHA', 'IND', 'BKN', 'ORL', 'MIA', 
             'WAS', 'PHI', 'MIL', 'NOP', 'MEM', 'DAL', 'ATL', 'UTA', 'DEN', 'SAS', 
             'MIN', 'POR', 'PHX', 'SAC', 'TOR', 'CHI', 'OKC', 'NYK', 'LAL', 'LAC')

# Plot
ggnet2(net, node.size = followers, node.color = teams,
       edge.size = 0.1, edge.color = "grey", 
       mode = 'fruchtermanreingold', 
       arrow.size = 4, arrow.gap = 0.005, 
       label = player_names, label.size = 5, label.color = 'grey28', 
       palette = y) + 
    theme(legend.position = "none")
