library(shiny)
library(tidyverse)
if(!require(igraph)) install.packages("igraph", repos = "http://cran.us.r-project.org")
if(!require(ggraph)) install.packages("ggraph", repos = "http://cran.us.r-project.org")
if(!require(DT)) install.packages("DT", repos = "http://cran.us.r-project.org")



# source("./network/getNet.R", local=TRUE)
# source("./network/plotNet.R", local=TRUE)
# source("./network/analNet.R", local=TRUE)

docs = read_csv('../../data/combinedData.csv');
target = read_csv('../../data/combinedTarget.csv');
claimTrack = read_csv('../../data/claimTrack.csv');

data = docs %>% 
  left_join(target, by=c('Provider','Set')) %>% 
  select(-c('X1.x','X1.y'));


################################################################################################
states = sort(c("Pennsylvania", "Alabama", "Texas", "New Jersey", 
           "Minnesota", "Oregon", "North Carolina", "Arizona", "Florida", 
           "Virginia", "Nevada", "California", "Illinois", "Michigan", "Missouri", 
           "New York", "Tennessee", "Ohio", "Wisconsin", "Indiana", "Colorado", 
           "Washington", "Massachusetts", "Louisiana", "Connecticut", "South Carolina", 
           "New Hampshire", "West Virginia", "Arkansas", "Kansas", "South Dakota", 
           "New Mexico", "North Dakota", "Kentucky", "Iowa", "Mississippi", 
           "Georgia", "Maine", "Montana", "Idaho", "Nebraska", "Puerto Rico", 
           "Utah", "Oklahoma", "Alaska", "Maryland", "Rhode Island", "District of Columbia", 
           "Wyoming", "Vermont", "Hawaii", "Delaware"))

################################################################################################
propat = function(data, state, county, status){
  if(county == 'all'){
    data.filt = 
      data %>% filter(State %in% state, Status %in% status)
  } else {
    data.filt = 
      data %>% filter(State %in% state, Status %in% status, County %in% county)
  }
  data.filt = 
    data.filt %>% 
    dplyr::select(Provider, PotentialFraud, BeneID, InscClaimAmtReimbursed,WhetherDead) %>%
    group_by(Provider, PotentialFraud, BeneID,WhetherDead) %>% 
    summarise(weights = sum(InscClaimAmtReimbursed)) %>% data.frame()
  
  ## Get Provider | Beneficiary
  connections = data.filt %>% dplyr::select(Provider,BeneID,WhetherDead,weights)
  ## Create bipartite graph
  Bnet <- graph_from_data_frame(connections,directed=FALSE)
  ## Add attribues
  shapes <- c(21,15)
  fraud = data.filt %>% select(Provider,PotentialFraud)
  V(Bnet)$type <- V(Bnet)$name %in% connections[,1]
  V(Bnet)$actor <- ifelse(V(Bnet)$name %in% connections[,1],'Provider','Patient')
  V(Bnet)$fraud <- ifelse(V(Bnet)$name %in% fraud[,1],fraud[,2],'Patient')
  #V(Bnet)$fraud <- factor(V(Bnet)$fraud, levels = c('Yes','?','No','Patient'))
  V(Bnet)$size <- 4*sqrt(strength(Bnet))
  V(Bnet)$shape <- shapes[V(Bnet)$type+1]
  
  FraudYes = V(Bnet)[fraud=='Yes']
  FraudNo = V(Bnet)[fraud=='No']
  FraudTest = V(Bnet)[fraud=='?']
  Patients = V(Bnet)[fraud=='Patient']
  
  V(Bnet)[fraud=='Yes']$color = "#e65247" # red
  V(Bnet)[fraud=='No']$color = "#57bf37" #green
  V(Bnet)[fraud=='?']$color = "#b24ed4" #purple
  V(Bnet)[fraud=='Patient']$color = "#3b68ff" #blue
  
  E(Bnet)[FraudYes %--% Patients]$color = "#e65247" # red
  E(Bnet)[FraudNo %--% Patients]$color = "#57bf37" #green
  E(Bnet)[FraudTest %--% Patients]$color = "#b24ed4" #purple
  return(Bnet)
}

################################################################################################
prodoc = function(data, state, county, status){
  if(county == 'all'){
    data.filt = 
      data %>% filter(State %in% state, Status %in% status)
  } else {
    data.filt = 
      data %>% filter(State %in% state, Status %in% status, County %in% county)
  }
  data.filt = 
    data.filt %>% 
    dplyr::select(Provider, PotentialFraud,InscClaimAmtReimbursed,
                  AttendingPhysician, OperatingPhysician, OtherPhysician) %>% 
    pivot_longer(cols=c(AttendingPhysician,OperatingPhysician,OtherPhysician), 
                 names_to = "Type", values_to = "Doctor") %>%
    filter(complete.cases(.)) %>% 
    group_by(Provider, PotentialFraud, Doctor) %>% 
    summarise(weights = sum(InscClaimAmtReimbursed)) %>% data.frame()
  
  ## Get Provider | Beneficiary
  connections = data.filt %>% dplyr::select(Provider,Doctor,weights)
  ## Create bipartite graph
  Bnet <- graph_from_data_frame(connections,directed=FALSE)
  ## Add attributes
  shapes <- c(25,15)
  fraud = data.filt %>% select(Provider,PotentialFraud)
  V(Bnet)$type <- V(Bnet)$name %in% connections[,1]
  V(Bnet)$actor <- ifelse(V(Bnet)$name %in% connections[,1],'Provider','Doctor')
  V(Bnet)$fraud <- ifelse(V(Bnet)$name %in% fraud[,1],fraud[,2],'Doctor')
  #V(Bnet)$fraud <- factor(V(Bnet)$fraud, levels =c('Yes','?','No','Doctor'))
  V(Bnet)$size <- 4*sqrt(strength(Bnet))
  V(Bnet)$shape <- shapes[V(Bnet)$type+1]
  
  FraudYes = V(Bnet)[fraud=='Yes']
  FraudNo = V(Bnet)[fraud=='No']
  FraudTest = V(Bnet)[fraud=='?']
  Doctors = V(Bnet)[fraud=='Doctor']
  
  V(Bnet)[fraud=='Yes']$color = "#e65247" # red
  V(Bnet)[fraud=='No']$color = "#57bf37" #green
  V(Bnet)[fraud=='?']$color = "#b24ed4" #purple
  V(Bnet)[fraud=='Doctor']$color = "#3b68ff" #blue
  
  E(Bnet)[FraudYes %--% Doctors]$color = "#e65247" # red
  E(Bnet)[FraudNo %--% Doctors]$color = "#57bf37" #green
  E(Bnet)[FraudTest %--% Doctors]$color = "#b24ed4" #purple
  return(Bnet)
}

################################################################################################
patdoc = function(data, state, county,status){
  if(county == 'all'){
    data.filt = 
      data %>% filter(State %in% state, Status %in% status)
  } else {
    data.filt = 
      data %>% filter(State %in% state, Status %in% status, County %in% county)
  }
  data.filt = 
    data.filt %>% 
    dplyr::select(BeneID, InscClaimAmtReimbursed,
                  AttendingPhysician, OperatingPhysician, OtherPhysician) %>% 
    pivot_longer(cols=c(AttendingPhysician,OperatingPhysician,OtherPhysician), 
                 names_to = "Type", values_to = "Doctor") %>%
    filter(complete.cases(.)) %>% 
    group_by(BeneID, Doctor) %>% 
    summarise(weights = sum(InscClaimAmtReimbursed)) %>% data.frame()
  
  ## Get Provider | Beneficiary
  connections = data.filt %>% dplyr::select(BeneID,Doctor,weights)
  ## Create bipartite graph
  Bnet <- graph_from_data_frame(connections,directed=FALSE)
  ## Add attributes
  shapes <- c(25,21)
  V(Bnet)$type <- V(Bnet)$name %in% connections[,1]
  V(Bnet)$actor <- ifelse(V(Bnet)$name %in% connections[,1],'Patient','Doctor')
  V(Bnet)$size <- 4*sqrt(strength(Bnet))
  V(Bnet)$shape <- shapes[V(Bnet)$type+1]
  
  
  V(Bnet)[actor=='Patient']$color = "#57bf37" #green
  V(Bnet)[actor=='Doctor']$color = "#3b68ff" #blue
  
  return(Bnet)
}

################################################################################################
### Duplication Network
target = target %>% distinct(Provider,PotentialFraud) %>% data.frame()
edges = claimTrack %>% 
  #filter(State_S %in% state, State_R %in% c('New York')) %>% 
  select(Sender,Receiver)
Dnet = edges %>% graph_from_data_frame(directed = TRUE)
Dnet = simplify(Dnet)
#V(Dnet)$type <- ifelse(V(Dnet)$name %in% edges[,1],'Sender','Receiver')

V(Dnet)$size <- sqrt(strength(Dnet))

V(Dnet)$fraud = ifelse(V(Dnet)$name %in% target[,1],target[,2],'?')


V(Dnet)[fraud=='Yes']$color = "#e65247" # red
V(Dnet)[fraud=='No']$color = "#57bf37" #green
V(Dnet)[fraud=='?']$color = "#b24ed4" #purple


################################################################################################
################################################################################################

plotDnet = function(dnet, layout = 'stress'){
  ggraph(dnet, layout = layout)+
    geom_edge_fan0(arrow = arrow(angle = 30, 
                                  length = unit(0.06, "inches"),
                                  ends = "last", type = "closed"),
                    alpha=0.3) +
    geom_node_point(
      aes(size = size, color = color),
      shape = 20,
      alpha=0.5,
      color = V(dnet)$color
      ) +
    geom_node_text(aes(filter = size >= 5, label = name, size=5),family="serif", repel=TRUE)+
    scale_edge_width_continuous(range = c(0.5,5), guide=FALSE)+
    scale_size_continuous(range = c(2,7), guide=FALSE)+
    theme_graph()
}

plotProPat = function(bnet, state, county, layout){
  
  ggraph(bnet, layout = layout)+
    geom_edge_link0(
      edge_alpha=0.3, 
      edge_color = E(bnet)$color, 
      aes(edge_width = weights)) + 
    geom_node_point(
      aes(size = size), 
      shape = V(bnet)$shape, 
      color = V(bnet)$color) +
    #geom_node_text(aes(filter = size >= 100, label = name, size=3),family="serif", repel=TRUE)+
    scale_edge_width_continuous(range = c(0.2,4), guide=FALSE)+
    scale_size_continuous(range = c(2,6), guide=FALSE)+
    theme_graph()
}

################################################################################################
plotProDoc = function(bnet, state, county, layout){
  
  ggraph(bnet, layout = layout)+
    geom_edge_link0(
      edge_alpha=0.3, 
      edge_color = E(bnet)$color, 
      aes(edge_width = weights)) + 
    geom_node_point(
      aes(size = size), 
      shape = V(bnet)$shape, 
      color = V(bnet)$color) +
    #geom_node_text(aes(filter = size >= 100, label = name, size=3),family="serif", repel=TRUE)+
    scale_edge_width_continuous(range = c(0.2,4), guide=FALSE)+
    scale_size_continuous(range = c(2,6), guide=FALSE)+
    theme_graph()
}

################################################################################################
plotPatDoc = function(bnet, state, county, layout){
  
  ggraph(bnet, layout = layout)+
    geom_edge_link0(
      edge_alpha=0.3, 
      #edge_color = E(bnet)$color, 
      aes(edge_width = weights)) + 
    geom_node_point(
      aes(size = size), 
      shape = V(bnet)$shape, 
      color = V(bnet)$color) +
    #geom_node_text(aes(filter = size >= 100, label = name, size=3),family="serif", repel=TRUE)+
    scale_edge_width_continuous(range = c(0.2,4), guide=FALSE)+
    scale_size_continuous(range = c(2,6), guide=FALSE)+
    theme_graph()
}

################################################################################################
plotActor = function(net, title, layout = 'tree', actor = 'provider'){
  
  if (actor=='provider') {
    shape = 15
  } else if (actor == 'patient') {
    shape = 21
  } else if (actor == 'doctor') {
    shape = 17
  }
  ggraph(net, layout = layout)+
    geom_edge_link0(edge_alpha=0.5, edge_colour = "grey66") + 
    geom_node_point(
      aes(size = size),
      color = V(net)$color,
      shape = shape) + 
    scale_edge_width_continuous(range = c(0.2,3), guide=FALSE)+
    scale_size_continuous(range = c(2,6), guide=FALSE) +
    theme_graph() +
    ggtitle(title)
}
