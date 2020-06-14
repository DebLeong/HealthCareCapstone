#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(ggraph)
library(igraph)
library(shiny)

ui <- fluidPage(
    plotOutput("plot", brush = brushOpts(id = "plot_brush"))
)

server <- function(input, output) {
    graph <- graph_from_data_frame(highschool)
    
    output$plot <- renderPlot({
        ggraph(graph) + 
            geom_edge_link(aes(colour = factor(year))) + 
            geom_node_point()
    })
    
    observe(print(
        brushedPoints(as_data_frame(graph, what = "vertices"), input$plot_brush)
    )
    )
}

shinyApp(ui, server)
