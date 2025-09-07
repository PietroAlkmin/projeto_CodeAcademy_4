import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")# leio o csv e converto 'date' pra datetime e uso como índice

# Clean data
df = df[(df["value"] >= df["value"].quantile(0.025)) & (df["value"] <= df["value"].quantile(0.975))]# Aqui eu removo os outliers (abaixo do 2.5% e acima do 97.5%) - Precisei de ajuda na sintaxe


def draw_line_plot():
    # Draw line plot
    # Estou usando o matplotlib para gerar uma imagem parecida com a fornecida nos exemplos(figura 1)
    #Precisei de ajuda para seguir a estrutura da criação do gráfico
    fig, ax = plt.subplots(figsize=(17, 7))
    ax.plot(df.index, df["value"])
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    # crio média mensal por ano (tabela ano x mês)
    df_bar = df.copy()
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month
    df_bar = (df_bar.groupby(["year", "month"])["value"].mean().unstack())# Aqui os meses viram colunas

    # Draw bar plot
    # reordeno meses e renomeio as colunas para nomes completos
    # precisei de ajudar para essa lógica
    # Aqui nos estamos substituindo os index meses por seus respectivos nomes completos
    df_bar = df_bar.reindex(columns=range(1, 13))
    df_bar.columns = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    ax = df_bar.plot(kind="bar", figsize=(12, 8), legend=True)
    fig = ax.get_figure()
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title="Months")

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    # dois boxplots: por ano (tendência) e por mês (sazonalidade)
    fig, axes = plt.subplots(1, 2, figsize=(13, 8))

    # ano
    sns.boxplot(data=df_box, x="year", y="value", ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # mês (ordem Jan..Dec)
    order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sns.boxplot(data=df_box, x="month", y="value", order=order, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
