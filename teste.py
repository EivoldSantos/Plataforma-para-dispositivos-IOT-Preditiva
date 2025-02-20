import plotly.express as px
import pandas as pd

# Preparação dos dados
data = {
    'Valores': [1, 2, 2, 3, 3, 3, 4, 4, 5]
}
df = pd.DataFrame(data)

# Criação do histograma
fig = px.histogram(df, x='Valores', nbins=5)

# Personalização do gráfico
fig.update_layout(
    title='Histograma de Valores',
    xaxis_title='Valores',
    yaxis_title='Frequência'
)

# Exibição do gráfico
fig.show()