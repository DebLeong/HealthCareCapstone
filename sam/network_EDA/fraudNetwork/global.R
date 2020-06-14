library(shiny)
library(tidyverse)


# source("./network/getNet.R", local=TRUE)
# source("./network/plotNet.R", local=TRUE)
# source("./network/analNet.R", local=TRUE)

docs = read_csv('../../data/combinedData.csv');
target = read_csv('../../data/combinedTarget.csv');

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
propat = function(data, state, county){
  if(county == 'all'){
    county = data %>%
      filter(State %in% state) %>%
      distinct(County) %>% pull
  }
  
  data.filt = 
    data %>% filter(State %in% state, County %in% county) %>% 
    dplyr::select(Provider, PotentialFraud, ClaimID, BeneID, WhetherDead) %>% 
    group_by(Provider, PotentialFraud, BeneID, WhetherDead) %>% 
    tally() %>% rename('weights' = 'n') %>% data.frame()
  
  ## Get Provider | Beneficiary
  connections = data.filt %>% dplyr::select(Provider,BeneID,weights)
  ## Create bipartite graph
  Bnet <- graph.data.frame(connections,directed=FALSE)
  ## Add attribues
  shapes <- c(21,15)
  fraud = data.filt %>% select(Provider,PotentialFraud)
  V(Bnet)$type <- V(Bnet)$name %in% connections[,1]
  V(Bnet)$actor <- ifelse(V(Bnet)$name %in% connections[,1],'Provider','Patient')
  V(Bnet)$fraud <- ifelse(V(Bnet)$name %in% fraud[,1],fraud[,2],'Patient')
  V(Bnet)$fraud <- factor(V(Bnet)$fraud, levels = c('Yes','?','No','Patient'))
  V(Bnet)$size <- degree(Bnet)
  V(Bnet)$shape <- shapes[V(Bnet)$type+1]
  # Create 4 new features for connectivity of providers based on bipartite projection graphs based on 
  # doctor and patient networks
  return(Bnet)
}

################################################################################################
prodoc = function(data, state, county){
  if(county == 'all'){
    county = data %>% 
      filter(State %in% state) %>% 
      distinct(County) %>% pull
  }
  data.filt = 
    data %>% filter(State %in% state, County %in% county) %>% 
    dplyr::select(Provider, PotentialFraud, ClaimID, 
                  AttendingPhysician, OperatingPhysician, OtherPhysician) %>% 
    pivot_longer(cols=c(AttendingPhysician,OperatingPhysician,OtherPhysician), 
                 names_to = "Type", values_to = "Doctor") %>%
    filter(complete.cases(.)) %>% 
    group_by(Provider, PotentialFraud, Doctor) %>% 
    tally() %>% rename('weights' = 'n') %>% data.frame()
  
  ## Get Provider | Beneficiary
  connections = data.filt %>% dplyr::select(Provider,Doctor,weights)
  ## Create bipartite graph
  Bnet <- graph.data.frame(connections,directed=FALSE)
  ## Add attributes
  shapes <- c(25,15)
  fraud = data.filt %>% select(Provider,PotentialFraud)
  V(Bnet)$type <- V(Bnet)$name %in% connections[,1]
  V(Bnet)$actor <- ifelse(V(Bnet)$name %in% connections[,1],'Provider','Doctor')
  V(Bnet)$fraud <- ifelse(V(Bnet)$name %in% fraud[,1],fraud[,2],'Doctor')
  V(Bnet)$fraud <- factor(V(Bnet)$fraud, levels =c('Yes','?','No','Doctor'))
  V(Bnet)$size <- degree(Bnet)
  
  V(Bnet)$shape <- shapes[V(Bnet)$type+1]
  # Create 4 new features for connectivity of providers based on bipartite projection graphs based on 
  # doctor and patient networks
  return(Bnet)
}

################################################################################################
patdoc = function(data, state, county){
  if(county == 'all'){
    county = data %>% 
      filter(State %in% state) %>% 
      distinct(County) %>% pull
  }
  
  data.filt = 
    data %>% filter(State %in% state, County %in% county) %>% 
    dplyr::select(ClaimID, BeneID, 
                  AttendingPhysician, OperatingPhysician, OtherPhysician) %>% 
    pivot_longer(cols=c(AttendingPhysician,OperatingPhysician,OtherPhysician), 
                 names_to = "Type", values_to = "Doctor") %>%
    filter(complete.cases(.)) %>% 
    group_by(BeneID, Doctor) %>% tally() %>% rename('weights' = 'n') %>% data.frame()
  
  ## Get Provider | Beneficiary
  connections = data.filt %>% dplyr::select(BeneID,Doctor,weights)
  ## Create bipartite graph
  Bnet <- graph.data.frame(connections,directed=FALSE)
  ## Add attributes
  shapes <- c(25,21)
  V(Bnet)$type <- V(Bnet)$name %in% connections[,1]
  V(Bnet)$size <- degree(Bnet)
  V(Bnet)$shape <- shapes[V(Bnet)$type+1]
  # Create 4 new features for connectivity of providers based on bipartite projection graphs based on 
  # doctor and patient networks
  return(Bnet)
}

################################################################################################
################################################################################################

plotProPat = function(bnet, state, county, layout){
  
  ggraph(bnet, layout = layout)+
    geom_edge_link0(alpha=0.5, edge_colour = "grey66", aes(width = weights)) + 
    geom_node_point(aes(
      #fitler = size >= 10,
      color = fraud,
      size = size), shape = V(bnet)$shape) +
    geom_node_text(aes(filter = size >= 50, label = name, size=3),family="serif", repel=TRUE)+
    scale_color_brewer(palette = "Set1",
                       name = "Fraud", labels=c('Yes','?','No','Patient'))+
    scale_edge_width_continuous(range = c(0.2,3), guide=FALSE)+
    scale_size_continuous(range = c(2,6), guide=FALSE)+
    theme_graph() +theme(legend.position = "left")
}

################################################################################################
plotProDoc = function(bnet, state, county, layout){
  
  ggraph(bnet, layout = layout)+
    geom_edge_link0(alpha=0.5, edge_colour = "grey66", aes(width = weights)) + 
    geom_node_point(aes(
      #fitler = size >= 10,
      color = fraud,
      size = size), shape = V(bnet)$shape) +
    geom_node_text(aes(filter = size >= 50, label = name, size=3),family="serif", repel=TRUE)+
    scale_color_brewer(palette = "Set1",
                       name = "Fraud", labels=c('Yes','?','No','Doctor'))+
    scale_edge_width_continuous(range = c(0.2,3), guide=FALSE)+
    scale_fill_manual(values = palette) +
    scale_size_continuous(range = c(2,6), guide=FALSE)+
    theme_graph() + theme(legend.position = "left")
}

################################################################################################
plotPatDoc = function(bnet, state, county, layout){
  ggraph(bnet, layout = layout)+
    geom_edge_link0(alpha=0.5, edge_colour = "grey66", aes(width = weights)) + 
    geom_node_point(aes(
      #fitler = size >= 10,
      #color = fraud,
      size = size), shape = V(bnet)$shape) +
    geom_node_text(aes(filter = size >= 50, label = name, size=3),family="serif", repel=TRUE)+
    scale_edge_width_continuous(range = c(0.2,3), guide=FALSE)+
    scale_fill_manual(values = palette) +
    scale_size_continuous(range = c(2,6), guide=FALSE) +
    theme_graph() + theme(legend.position = "right")
}

################################################################################################
plotActor = function(net, title, layout = 'stress', provider = FALSE){
  g= ggraph(net, layout = layout)+
    geom_edge_link0(alpha=0.5, edge_colour = "grey66")
  if (provider){
    g + geom_node_point(aes(
      #fitler = size >= 10,
      color = fraud,
      size = size)) +
      #geom_node_text(aes(filter = size >= 10, label = name, size=3),family="serif", repel=TRUE)+
      scale_edge_width_continuous(range = c(0.2,3), guide=FALSE)+
      scale_size_continuous(range = c(2,6), guide=FALSE) +
      theme_graph() + theme(legend.position = "right") +
      ggtitle(title)
  } else {
    g + geom_node_point(aes(
      #fitler = size >= 10,
      #color = fraud,
      size = size)) +
      #geom_node_text(aes(filter = size >= 10, label = name, size=3),family="serif", repel=TRUE)+
      scale_color_brewer(palette = "Set1",
                           name = "Fraud", labels=c('Yes','?','No'))+
      scale_edge_width_continuous(range = c(0.2,3), guide=FALSE)+
      scale_size_continuous(range = c(2,6), guide=FALSE) +
      theme_graph() + theme(legend.position = "right") + 
      ggtitle(title)
  }
}
