## Ejemplo de codigo con plotly
import plotly.express as px
df = px.data.gapminder()
fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", 
                size="pop", color="continent", hover_name="country",
                log_x=True, size_max=55, range_y=[25,90])
fig.show()