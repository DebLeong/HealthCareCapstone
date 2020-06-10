
plotProPat = function(bnet, layout = 'stress', save = FALSE){
  
  #palette <- c('?'="#1A5878",'Patient'= "#C44237", 'No' = "#AD8941", 'Yes' = "green")
  
  #id_palette <- c("#1A5878","#C44237","#AD8941","green")
  ggraph(bnet, layout = layout)+
    geom_edge_link0(alpha=0.5, edge_colour = "grey66", aes(width = weights)) + 
    #geom_node_point(aes(color = fraud, size = size), shape = V(bnet)$shape) +
    geom_node_point(aes(
      #fitler = size >= 10,
      color = fraud,
      size = size), shape = V(bnet)$shape) +
    geom_node_text(aes(filter = size >= 50, label = name, size=3),family="serif", repel=TRUE)+
    scale_color_brewer(palette = "Dark2")+
    scale_edge_width_continuous(range = c(0.2,3), guide=FALSE)+
    scale_fill_manual(values = palette) +
    scale_size_continuous(range = c(1,5), guide=FALSE)+
    theme_graph() +
    theme(legend.position = "bottom")
  
    #ggsave(filename=paste0('./visualizations/networks/pb_5_200_sugiyama.png'),plot=last_plot())
}

plotProDoc = function(bnet, layout = 'stress', save = FALSE){
  
  #palette <- c('?'="#1A5878",'Patient'= "#C44237", 'No' = "#AD8941", 'Yes' = "green")
  
  #id_palette <- c("#1A5878","#C44237","#AD8941","green")
  ggraph(bnet, layout = layout)+
    geom_edge_link0(alpha=0.5, edge_colour = "grey66", aes(width = weights)) + 
    #geom_node_point(aes(color = fraud, size = size), shape = V(bnet)$shape) +
    geom_node_point(aes(
      #fitler = size >= 10,
      color = fraud,
      size = size), shape = V(bnet)$shape) +
    geom_node_text(aes(filter = size >= 50, label = name, size=3),family="serif", repel=TRUE)+
    scale_color_brewer(palette = "Dark2")+
    scale_edge_width_continuous(range = c(0.2,3), guide=FALSE)+
    scale_fill_manual(values = palette) +
    scale_size_continuous(range = c(1,5), guide=FALSE)+
    theme_graph() +
    theme(legend.position = "bottom")
  
  #ggsave(filename=paste0('./visualizations/networks/pb_5_200_sugiyama.png'),plot=last_plot())
}

plotPatDoc = function(bnet, layout = 'stress', save = FALSE){
  
  #palette <- c('?'="#1A5878",'Patient'= "#C44237", 'No' = "#AD8941", 'Yes' = "green")
  
  #id_palette <- c("#1A5878","#C44237","#AD8941","green")
  ggraph(bnet, layout = layout)+
    geom_edge_link0(alpha=0.5, edge_colour = "grey66", aes(width = weights)) + 
    #geom_node_point(aes(color = fraud, size = size), shape = V(bnet)$shape) +
    geom_node_point(aes(
      #fitler = size >= 10,
      #color = fraud,
      size = size), shape = V(bnet)$shape) +
    geom_node_text(aes(filter = size >= 50, label = name, size=3),family="serif", repel=TRUE)+
    #scale_color_brewer(palette = "Dark2")+
    scale_edge_width_continuous(range = c(0.2,3), guide=FALSE)+
    scale_fill_manual(values = palette) +
    scale_size_continuous(range = c(1,5), guide=FALSE)+
    theme_graph() +
    theme(legend.position = "bottom")
  
  #ggsave(filename=paste0('./visualizations/networks/pb_5_200_sugiyama.png'),plot=last_plot())
}