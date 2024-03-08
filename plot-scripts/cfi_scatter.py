import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import math
import random
import sys
#pd.options.mode.chained_assignment = None  # default='warn'

# Specify the directory path
# directory_path = ""  # Replace with the actual path

# ssl_server2.0.0.preopt.bc-call-targets-pwc.csv
def create_categories(files):
    app_map = {}
    for filename in files:
        # Split the filename by "." to separate the parts
        parts = filename.split(".")
        app_name = parts[0]

        if len(parts) >= 2:
            # Split parts[0] by "-" to separate the application name and the last modifier
            app_parts = parts[-2].split("-")
            if len(app_parts) >= 2:
                # Extract the last modifier (e.g., default, full, vgep, pwc)
                last_modifier = app_parts[-1]
                if app_name not in app_map:
                    app_map[app_name] = {}
                app_map[app_name][last_modifier] = filename
    return app_map

def plot_figs(dfs):
    X_axis = np.arange(len(dfs))

    m = 2
    n = 5
    fig, axes = plt.subplots(m, n, figsize=(11, 4.3) ,
            gridspec_kw={'height_ratios': [50, 50], 'width_ratios' :
                [20,20,20,20,20]})

    # patterns =('++', '///', 'xx' , '||','--', '..', '+-', 'xxxx', '....') #,'\\','\\\\'

    patterns =('++++', '////', 'xxxx' , '....', '--', '..', '+-', '\\\\\\') #,'\\','\\\\'

    colors = ["#75eab6", "#33547a", "#88aee1", "#862593", "#FF0000",
            "#F42912", "#2D402D", "#2712AB"]
    apps = ['ssl_server2', 'tiffcp', 'lighttpd',
            'memcached-libevent', 'pngcp', 'xmllint-full', 'wget', 'dtls-server']

    apps_map = {'ssl_server2':'MbedTLS', 'tiffcp':'Libtiff',
            'curl':'Curl', 'lighttpd':'Lighttpd',
            'memcached-libevent':'Memcached', 'pngcp':'LibPNG',
            'xmllint-full':'Libxml', 'wget':'Wget', 'dtls-server':'TinyDTLS'}


    labels = ['Baseline', 'Kaleidoscope']
    elements = []

    app_index = 0
    cmap = plt.cm.get_cmap('viridis')

    """
    'dtls-server'
    'lighttpd'
    'memcached-libevent'
    'pngcp'
    'ssl_server2'
    'tiffcp'
    'wget'
    'xmllint-full'
    """
    app_avg_data_map = {}
    app_max_data_map = {}

    avg_factor_impr_arr = []
    max_factor_impr_arr = []

    for i in range(0, m):
        for j in range(0, n):
            if app_index >= len(apps):
                break
            app = apps[app_index]
            print (app)
            if app not in dfs:
                app_index = app_index + 1
                continue

            baseline = [int(x) for x in dfs[app]['default']]
            full = [int(x) for x in dfs[app]['full']]

            complete_data = [baseline, full]

            avg_baseline = round(sum(baseline)/len(baseline), 2)
            avg_full = round(sum(full)/len(full), 2)


            avg_factor_impr = round(avg_baseline/avg_full, 2)
            avg_factor_impr_arr.append(avg_factor_impr)

            max_baseline = max(baseline)
            max_full = max(full)



            max_factor_impr = round(max_baseline/max_full, 2)
            max_factor_impr_arr.append(max_factor_impr)

            avg_data_arr = [avg_baseline, avg_full,
                    avg_factor_impr]
            max_data_arr = [max_baseline, max_full, max_factor_impr]
 
            """
            data_arr = [avg_baseline, avg_ctx, avg_vgep, avg_pwc,
                    avg_ctx_vgep, avg_ctx_pwc, avg_pwc_vgep, avg_full,
                    avg_factor_impr, max_baseline, max_ctx, max_vgep, max_pwc,
                    max_ctx_vgep, max_ctx_pwc, max_pwc_vgep,
                    max_full, max_factor_impr]
            """
            
            arr_map = {1: baseline, 2:full}
            # print(complete_data)
            bp = axes[i][j].boxplot(complete_data, showmeans=True, meanline=True,
                            flierprops={'marker': '+', 'markersize': 3},
                            whis=4, patch_artist=True,
                            medianprops={'linestyle': '', 'color': 'none'},
                            meanprops={"linewidth": 2} )
            elements.append(bp)
            # bp = axes[i][j].violinplot(complete_data)

            """
            outliers = bp["fliers"]
            for outlier in outliers:
                x_data = outlier.get_xdata()
                y_data = outlier.get_ydata()
                for (x,y) in zip(x_data, y_data):
                    print ("x = " + str(x) + " y = " + str(y))
                    if arr_map[x].count(y) > 50:
                        print("Setting label")
                        outlier.set_label(str(arr_map[x].count(y)))
                        continue
            """
                    
            # axes[i][j].set_xticklabels(complete_data.keys())
            app_name = apps_map[apps[app_index]]
            print(app_name)

            app_avg_data_map[app_name] = avg_data_arr
            app_max_data_map[app_name] = max_data_arr

            axes[i][j].set_title(app_name, fontsize='10')

            # axes[i][j].bar(1, baseline, 0.3, label = "Baseline")
            # axes[i][j].bar(2, ctx, 0.3, label = "Kd-Ctx")
            # axes[i][j].bar(3, vgep, 0.3, label = "Kd-PA")
            # axes[i][j].bar(4, pwc, 0.3, label = "Kd-PWC")
            # axes[i][j].bar(5, full, 0.3, label = "Kaleidoscope")
            # axes[i][j].set_title(apps[app_index], fontsize='small')
            axes[i][j].set_xticks([])

            # Hatches
            boxes = bp['boxes']
            # print (bars)

            for box, color, pattern, label in zip(boxes, colors, patterns, labels):
                box.set_hatch(pattern)
                box.set_edgecolor(color)
                box.set_fill(False)
                box.set_label(label)

            medians = bp['medians']
            # print (bars)
            for median in medians:
                median.set_visible(False)
                #median.set_color("#FFFFFF")

            means = bp['means']
            for mean, color in zip(means, colors):
                mean.set_color(color)
            if j == 0:
                axes[i][j].set_ylabel('Number of Targets')
            app_index = app_index + 1

    # Remove the plots, this will give us space for our legend
    axes[1][3].set_visible(False)
    axes[1][4].set_visible(False)

    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=color, label=label, hatch=hatch)
            for color, label, hatch in zip(colors, labels,patterns)]
    
    for hatch, handle in zip(patterns, legend_handles):
        handle.set_hatch(hatch)
        handle.set_fill(False)

    fig.legend(handles=legend_handles, loc='lower right', frameon=False,
            bbox_to_anchor=(0.99,0.09), ncol=1)
    plt.subplots_adjust(right=0.85)
    fig.tight_layout()
    plt.savefig('./box-cfi.pdf')

    for i in range(len(apps)):
        app = apps_map[apps[i]]
        print(app, end=', ')
        for ind, data in enumerate(app_avg_data_map[app]):
            if ind == len(apps) - 1:
                print(data, end = ' ')
            else:
                print(data, end = ', ')
        print()


    print(sum(avg_factor_impr_arr))
    print("Average average improvement " +
            str(round(sum(avg_factor_impr_arr)/len(avg_factor_impr_arr), 2)))
    print("Average max improvement " +
            str(round(sum(max_factor_impr_arr)/len(max_factor_impr_arr), 2)))





#cfi_data = pd.read_csv('../data/cfi_avg.dat', names =  ['Application',
#    'Default-CFI', 'Kaleidoscope-Ctx', 'Kaleidoscope-PWC', 
#    'Kaleidoscope-PA', 'Kaleidoscope-Full', 'Perc-Impr'], header=0)
#
#plt.savefig('../figs/box-cfi.pdf')

def load_data(app_map):
    dfs = {} # Map of dataframes
    for app in app_map:
        for mod in app_map[app]:
            filename = app_map[app][mod]
            if app not in dfs:
                dfs[app] = {}
            with open(directory_path + "/" + filename) as f:
                dfs[app][mod] = f.read().splitlines()
    return dfs

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(0)
    directory_path = sys.argv[1]
    # List all files in the directory
    files = os.listdir(directory_path)
    
    # Filter files that end with "call-targets-*.csv"
    filtered_files = [filename for filename in files if "call-targets-" in filename]
    matplotlib.use('agg')
    plt.ioff()
    app_map = create_categories(filtered_files)
    cfi_data = load_data(app_map)
    plot_figs(cfi_data)
    # plot_sample(cfi_data)
