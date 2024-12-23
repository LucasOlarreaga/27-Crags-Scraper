import matplotlib.pyplot as plt
import shapefile
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
import sqlite3
import matplotlib.colors as mcolors

def load_data(column_name, sum_or_avg='sum'):
    conn = sqlite3.connect('files/merged_climbs.db')
    query = f'''
        SELECT country, {sum_or_avg.upper()}({column_name}) as total_{column_name}
        FROM climbs
        GROUP BY country
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def plot_input_per_country(df, column_name, log=False, sum_or_avg='sum'):
    # Load world map shapefile using pyshp
    world_path = 'files/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp'
    sf = shapefile.Reader(world_path)

    # Create a Cartopy map
    fig, ax = plt.subplots(1, 1, figsize=(15, 10), subplot_kw={'projection': ccrs.PlateCarree()})
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    # Normalize the ascents data for colormap
    max_input = df[f'total_{column_name}'].max()
    if log == True:
        norm = mcolors.LogNorm(vmin=1, vmax=max_input)
    elif log == False:
        norm = mcolors.Normalize(vmin=0, vmax=max_input)
    else:
        print("Error: log must be True or False")

    # Create a custom colormap
    colors = [(1, 0.8, 0.8), (0, 0.5, 0)]
    cmap = mcolors.LinearSegmentedColormap.from_list("custom_cmap", colors)

    # Print countries in shape_rec but not in df
    #shape_countries = set([shape_rec.record['NAME'] for shape_rec in sf.shapeRecords()])
    df_countries = set(df['country'].values)
    #missing_countries_df = pd.DataFrame(list(shape_countries - df_countries), columns=['country'])

    # Plot the ascents data
    for shape_rec in sf.shapeRecords():
        country_name = shape_rec.record['NAME']
        if country_name in df['country'].values:
            inputs = df[df['country'] == country_name][f'total_{column_name}'].values[0]
            if isinstance(inputs, float):
                inputs = round(inputs, 2)
            shape = shape_rec.shape
            lons, lats = zip(*shape.points)
            x, y = sum(lons) / len(lons), sum(lats) / len(lats)  # Calculate the centroid
            ax.text(x, y, inputs, transform=ccrs.PlateCarree(), fontsize=8, ha='center', fontweight='bold')

            parts = list(shape.parts) + [len(shape.points)]  # Ensure correct handling of parts
            color = cmap(norm(max(inputs, 0.1)))
            for i in range(len(parts) - 1):
                ax.fill(lons[parts[i]:parts[i+1]], lats[parts[i]:parts[i+1]], transform=ccrs.PlateCarree(), color=color, alpha=0.7)

    # Add a colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', pad=0.05, format='%.0f')

    operation = ''

    if sum_or_avg == 'SUM':
        operation = 'Total'
    elif sum_or_avg == 'AVG':
        operation = 'Average'
    else:
        print("Error: sum_or_avg must be 'SUM' or 'AVG'")

    cbar.set_label(f'{operation.capitalize()} {column_name.capitalize()}')
    plt.title(f'{operation.capitalize()} {column_name.capitalize()} per Country')
    plt.show()


if __name__ == "__main__":
   inputs = [
        {'parameter': 'ascents', 'operation': 'SUM', 'log': True},
        {'parameter': 'rating', 'operation': 'AVG', 'log': False},
        {'parameter': 'grade', 'operation': 'AVG', 'log': False}
    ]
   
   for input_dict in inputs:
        parameter = input_dict['parameter']
        operation = input_dict['operation']
        log = input_dict['log']
        df = load_data(parameter, operation)
        plot_input_per_country(df, parameter, log, operation)