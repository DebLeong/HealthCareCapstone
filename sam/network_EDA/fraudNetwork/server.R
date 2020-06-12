#
# This is the server logic of a Shiny web application. You can run the
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)

# Define server logic required to draw a histogram
shinyServer(function(input, output) {

    output$network = renderVisNetwork({
        load("../nodes.RData")
        load("../edges.RData")
    
        
        visNetwork(nodes, edges, width = "100%") %>%
            visIgraphLayout() %>%
            visNodes(
                shape = "dot",
                color = list(
                    background = "#0085AF",
                    border = "#013848",
                    highlight = "#FF8000"
                ),
                shadow = list(enabled = TRUE, size = 10)
            ) %>%
            visEdges(
                shadow = FALSE,
                color = list(color = "#0085AF", highlight = "#C62F4B")
            ) %>%
            visOptions(highlightNearest = list(enabled = T, degree = 1, hover = T),
                       selectedBy = "group") %>% 
            visLayout(randomSeed = 11)
    })

})
