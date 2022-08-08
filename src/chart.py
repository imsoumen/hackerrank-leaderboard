import bar_chart_race as bcr
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from IPython.display import HTML

sourcedf = pd.read_csv("leaderboard-data.csv").set_index('username').T.rename_axis('Date').reset_index().rename_axis(None, axis=1)
#sourcedf = pd.read_csv("leaderboard-data.csv", usecols=['username', 'Anisha_Priya1']).rename(columns={'username':'date'}).head(3).T
sourcedf.fillna(0.0, inplace=True)
#print(sourcedf)

##df = pd.read_csv('https://git.io/fjpo3', usecols=['name', 'group', 'year', 'value'])
#df.head(3)


# bcr.bar_chart_race(
#     df = sourcedf[:5],
#     filename = "video.gif"
# )

fig, ax = plt.subplots(figsize=(15, 8))
ax.barh(sourcedf['Date'], sourcedf['Anisha_Priya1'])
#fig.show()


fig, ax = plt.subplots(figsize=(15, 8))

colors = dict(zip(
    ["Anisha_Priya1", "Europe", "Asia", "Latin America", "Middle East", "North America", "Africa"],
    ["#adb0ff", "#ffb3ff", "#90d595", "#e48381", "#aafbff", "#f7bb5f", "#eafb50"]
))
group_lk = sourcedf.set_index('Date')['Anisha_Priya1'].to_dict()

def draw_barchart(current_year):
    dff = sourcedf[sourcedf['Date'].eq(current_year)].sort_values(by='Date', ascending=True).tail(10)
    ax.clear()
    ax.barh(dff['Date'], dff['Anisha_Priya1'], color=[colors[group_lk[x]] for x in dff['Date']])
    dx = dff['Anisha_Priya1'].max() / 200
    for i, (value, name) in enumerate(zip(dff['Anisha_Priya1'], dff['Date'])):
        ax.text(value-dx, i,     name,           size=14, weight=600, ha='right', va='bottom')
        ax.text(value-dx, i-.25, group_lk[name], size=10, color='#444444', ha='right', va='baseline')
        ax.text(value+dx, i,     f'{value:,.0f}',  size=14, ha='left',  va='center')
    ax.text(1, 0.4, current_year, transform=ax.transAxes, color='#777777', size=46, ha='right', weight=800)
    ax.text(0, 1.06, 'Population (thousands)', transform=ax.transAxes, size=12, color='#777777')
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=12)
    ax.set_yticks([])
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    ax.text(0, 1.15, 'The most populous cities in the world from 1500 to 2018',
            transform=ax.transAxes, size=24, weight=600, ha='left', va='top')
    ax.text(1, 0, 'by @pratapvardhan; credit @jburnmurdoch', transform=ax.transAxes, color='#777777', ha='right',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
    plt.box(False)

#draw_barchart(2022)

# fig, ax = plt.subplots(figsize=(15, 8))
# animator = animation.FuncAnimation(fig, draw_barchart, frames=range(1968, 2019))
# HTML(animator.to_jshtml()) 