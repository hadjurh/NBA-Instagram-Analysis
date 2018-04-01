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
dirname <- "NBA_Instagram_Analysis"
dirs <- list.dirs(path=file.path("~/Documents/"), recursive=T)
dir_wd <- names(unlist(sapply(dirs, grep, pattern=dirname))[1])
setwd(dir_wd)
rm(dirname,  dirs,  dir_wd)

# Get data
network <- read.csv2(file = 'database/all-stars_2018/adjacency_matrix.csv',  sep = ',', header = FALSE)
usernames <- scan(file = '../get_data_from_scraper/username_private_removed.txt', what = '', sep = '\n')
players <- c(
    "Aaron Gordon", "Al Horford", 
    "Al-Farouq Aminu", "Alex Abrines", 
    "Allen Crabbe", "Amir Johnson", 
    "Andre Drummond", "Andre Iguodala", 
    "Andrew Harrison", "Andrew Wiggins", 
    "Anthony Davis", "Anthony Tolliver", 
    "Aron Baynes", "Arron Afflalo", 
    "Austin Rivers", "Bam Adebayo", 
    "Ben McLemore", "Ben Simmons", 
    "Bismack Biyombo", "Blake Griffin", 
    "Bobby Portis", "Bogdan Bogdanovic", 
    "Bojan Bogdanovic", "Bradley Beal", 
    "Brandon Ingram", "Brandon Paul", 
    "Brook Lopez", "Bryn Forbes", 
    "Buddy Hield", "CJ McCollum", 
    "CJ Miles", "Carmelo Anthony", 
    "Cedi Osman", "Channing Frye", 
    "Chris Paul", "Clint Capela", 
    "Corey Brewer", "Cory Joseph", 
    "Courtney Lee", "Cristiano Felicio", 
    "Damian Lillard", "Daniel Theis", 
    "Danny Green", "Dante Cunningham", 
    "Dario Saric", "Darius Miller", 
    "Darren Collison", "David Nwaba", 
    "David West", "Davis Bertans", 
    "De'Aaron Fox", "DeAndre Jordan", 
    "DeAndre Liggins", "DeMar DeRozan", 
    "DeMarcus Cousins", "DeMarre Carroll", 
    "Dejounte Murray", "Delon Wright", 
    "Dennis Schroder", "Dennis Smith Jr.", 
    "Denzel Valentine", "Derrick Favors", 
    "Devin Booker", "Devin Harris", 
    "Dewayne Dedmon", "Deyonta Davis", 
    "Dillon Brooks", "Dirk Nowitzki", 
    "Domantas Sabonis", "Donovan Mitchell", 
    "Doug McDermott", "Dragan Bender", 
    "Draymond Green", "Dwayne Bacon", 
    "Dwight Howard", "Dwight Powell", 
    "Dwyane Wade", "E'Twaun Moore", 
    "Ed Davis", "Ekpe Udoh", 
    "Elfrid Payton", "Emmanuel Mudiay", 
    "Enes Kanter", "Eric Bledsoe", 
    "Eric Gordon", "Eric Moreland", 
    "Ersan Ilyasova", "Evan Fournier", 
    "Evan Turner", "Frank Kaminsky", 
    "Frank Mason", "Frank Ntilikina", 
    "Fred VanVleet", "Garrett Temple", 
    "Gary Harris", "George Hill", 
    "Giannis Antetokounmpo", "Goran Dragic", 
    "Gorgui Dieng", "Harrison Barnes", 
    "Hassan Whiteside", "Ian Clark", 
    "Ian Mahinmi", "Ish Smith", 
    "J.J. Barea", "JJ Redick", 
    "JR Smith", "JaMychal Green", 
    "JaVale McGee", "Jae Crowder", 
    "Jakob Poeltl", "Jamal Murray", 
    "Jameer Nelson", "James Harden", 
    "Jarell Martin", "Jarrett Allen", 
    "Jarrett Jack", "Jawun Evans", 
    "Jaylen Brown", "Jayson Tatum", 
    "Jeff Green", "Jerami Grant", 
    "Jeremy Lamb", "Jerian Grant", 
    "Jimmy Butler", "Joe Ingles", 
    "Joe Johnson", "Joel Embiid", 
    "Joffrey Lauvergne", "John Collins", 
    "John Henson", "Jonas Jerebko", 
    "Jonas Valanciunas", "Jonathon Simmons", 
    "Jordan Bell", "Jordan Clarkson", 
    "Jose Calderon", "Josh Hart", 
    "Josh Huestis", "Josh Jackson", 
    "Josh Richardson", "Jrue Holiday", 
    "Julius Randle", "Justin Holiday", 
    "Justin Jackson", "Justise Winslow", 
    "Jusuf Nurkic", "Karl-Anthony Towns", 
    "Kelly Olynyk", "Kelly Oubre Jr.", 
    "Kemba Walker", "Kent Bazemore", 
    "Kentavious Caldwell-Pope", "Kevin Durant", 
    "Kevin Love", "Kevon Looney", 
    "Khris Middleton", "Klay Thompson", 
    "Kosta Koufos", "Kristaps Porzingis", 
    "Kyle Anderson", "Kyle Korver", 
    "Kyle Kuzma", "Kyle Lowry", 
    "Kyle O'Quinn", "Kyrie Irving", 
    "LaMarcus Aldridge", "Lance Stephenson", 
    "Lance Thomas", "Langston Galloway", 
    "Larry Nance Jr.", "Lauri Markkanen", 
    "LeBron James", "Lonzo Ball", 
    "Lou Williams", "Luc Mbah a Moute", 
    "Luke Kennard", "Malcolm Brogdon", 
    "Malcolm Delaney", "Malik Beasley", 
    "Malik Monk", "Manu Ginobili", 
    "Marc Gasol", "Marcin Gortat", 
    "Marco Belinelli", "Marcus Morris", 
    "Marcus Smart", "Mario Chalmers", 
    "Mario Hezonja", "Markieff Morris", 
    "Marquese Chriss", "Marreese Speights", 
    "Mason Plumlee", "Maurice Harkless", 
    "Maxi Kleber", "Michael Beasley", 
    "Michael Carter-Williams", "Michael Kidd-Gilchrist", 
    "Miles Plumlee", "Montrezl Harrell", 
    "Myles Turner", "Nemanja Bjelica", 
    "Nene", "Nick Young", 
    "Nicolas Batum", "Nikola Jokic", 
    "Nikola Mirotic", "Noah Vonleh", 
    "Norman Powell", "OG Anunoby", 
    "Omri Casspi", "Otto Porter Jr.", 
    "PJ Tucker", "Pascal Siakam", 
    "Pat Connaughton", "Patrick McCaw", 
    "Patrick Patterson", "Patty Mills", 
    "Pau Gasol", "Paul George", 
    "Paul Zipser", "Quincy Acy", 
    "Rajon Rondo", "Raymond Felton", 
    "Reggie Bullock", "Ricky Rubio", 
    "Robert Covington", "Robin Lopez", 
    "Rodney Hood", "Rondae Hollis-Jefferson", 
    "Royce O'Neale", "Rudy Gay", 
    "Rudy Gobert", "Russell Westbrook", 
    "Ryan Anderson", "Salah Mejri", 
    "Sam Dekker", "Semi Ojeleye", 
    "Serge Ibaka", "Shabazz Napier", 
    "Shane Larkin", "Shaun Livingston", 
    "Shelvin Mack", "Skal Labissiere", 
    "Spencer Dinwiddie", "Stanley Johnson", 
    "Stephen Curry", "Sterling Brown", 
    "Steven Adams", "T.J. McConnell", 
    "TJ Leaf", "TJ Warren", 
    "Taj Gibson", "Taurean Prince", 
    "Terrance Ferguson", "Terry Rozier", 
    "Thon Maker", "Tim Frazier", 
    "Tim Hardaway Jr.", "Tobias Harris", 
    "Tomas Satoransky", "Tony Parker", 
    "Tony Snell", "Treveon Graham", 
    "Trevor Booker", "Trey Lyles", 
    "Tristan Thompson", "Troy Daniels", 
    "Tyler Dorsey", "Tyler Johnson", 
    "Tyler Ulis", "Tyreke Evans", 
    "Tyson Chandler", "Tyus Jones", 
    "Victor Oladipo", "Wayne Ellington", 
    "Wes Iwundu", "Wesley Matthews", 
    "Will Barton", "Willie Cauley-Stein", 
    "Wilson Chandler", "Zach Collins", 
    "Zach Randolph", "Zaza Pachulia"
)
teams <- scan(file = '../get_data_from_scraper/team_private_removed.txt', what = '', sep = '\n')
colors <- read.csv2(file = '../../NBA/r_data_analysis/team_colors.csv')

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
ggnet2(net, node.size = 6, node.color = teams,  
       edge.size = 0.2, edge.color = "grey", 
       mode = 'fruchtermanreingold', 
       arrow.size = 3, arrow.gap = 0.003, 
       label = players, label.size = 6, label.color = 'grey28', 
       palette = y)
