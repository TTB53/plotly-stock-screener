import plotly.graph_objects as go
import plotly.io as pio

# Theme Colors
IVORY = '#FEFFF1'
BLACK = '#333333'
DIMGREY = '#42403F'

AQUAMARINE = '#9BCEB5'
DARKCYAN = '#388895'
DARKSLATEGREEN = '#42403F'
AZURE = '#E4F2EF'
CADETBLUE = '#709784'  # This is actually a dark version for Aquamarine and a light version for DarkSlateGreen
DARKSLATECYAN = '#1f4f57'
GOLDENROD = '#cfa42f'
LIGHTGOLDENROD = "#d6c79f"
ROSYBROWN = "#ce9b9b"  # Red for Red-Green Contrasts

# various Colorscales based on Theme Colors. l

aqua_to_rosy = [
    [0, AQUAMARINE],
    [0.1, '#a9d2bd'],
    [0.2, '#b7d5c6'],
    [0.3, '#c5d9ce'],
    [0.4, '#d2dcd7'],
    [0.5, '#dfdfdf'],
    [0.6, '#ddd2d1'],
    [0.7, '#dac4c4'],
    [0.8, '#d6b6b6'],
    [0.9, '#d2a9a8'],
    [1, ROSYBROWN]
]
dark_slate_cyan_to_aqua = [
    [0, DARKSLATECYAN],
    [0.1, '#2B5C60'],
    [0.2, '#38686A'],
    [0.3, '#447573'],
    [0.4, '#51827D'],
    [0.5, '#5D8F86'],
    [0.6, '#699B8F'],
    [0.7, '#76A899'],
    [0.8, '#82B5A2'],
    [0.9, '#8FC1AC'],
    [1, AQUAMARINE]
]
gold_to_aqua = [
    [0, GOLDENROD],
    [0.1, '#CAA83C'],
    [0.2, '#C5AC4A'],
    [0.3, '#BFB157'],
    [0.4, '#BAB565'],
    [0.5, '#B5B972'],
    [0.6, '#B0BD7F'],
    [0.7, '#ABC18D'],
    [0.8, '#A5C69A'],
    [0.9, '#A0CAA8'],
    [1, AQUAMARINE]
]
dark_cyan_to_aqua = [
    [0, DARKCYAN],
    [0.1, '#428F98'],
    [0.2, '#4C969B'],
    [0.3, '#569D9F'],
    [0.4, '#60A4A2'],
    [0.5, '#6AABA5'],
    [0.6, '#73B2A8'],
    [0.7, '#7DB9AB'],
    [0.8, '#87C0AF'],
    [0.9, '#91C7B2'],
    [1, AQUAMARINE]
]
cadet_to_aqua_seq = [
                        [0.0, CADETBLUE],
                        [0.1111111111111111, '#749C89'],
                        [0.2222222222222222, '#79A28E'],
                        [0.3333333333333333, '#7DA893'],
                        [0.4444444444444444, '#81AD98'],
                        [0.5555555555555556, '#86B39D'],
                        [0.6666666666666666, '#8AB8A1'],
                        [0.7777777777777778, '#8EBEA6'],
                        [0.8888888888888888, '#92C3AB'],
                        [1.0, AQUAMARINE]
                    ]
cadet_to_aqua_seq_min = [
    [0.0, CADETBLUE],
    [0.1111111111111111, '#749C89'],
    [0.2222222222222222, '#79A28E'],
    [0.3333333333333333, '#7DA893'],
    [0.4444444444444444, '#81AD98'],
    [0.5555555555555556, '#86B39D'],
    [0.6666666666666666, '#8AB8A1'],
    [0.7777777777777778, '#8EBEA6'],
    [0.8888888888888888, '#92C3AB'],
    [1.0, AQUAMARINE]
]  # Reverse of seq
gol_to_aqua_seq = [
    [0.0, '#CFA42F'],
    [0.1111111111111111, '#CAA83C'],
    [0.2222222222222222, '#C5AC4A'],
    [0.3333333333333333, '#BFB157'],
    [0.4444444444444444, '#BAB565'],
    [0.5555555555555556, '#B5B972'],
    [0.6666666666666666, '#B0BD7F'],
    [0.7777777777777778, '#ABC18D'],
    [0.8888888888888888, '#A5C69A'],
    [1.0, '#9BCEB5']
]
dark_slate_green_to_aqua_seq = [
    [0.0, '#CFA42F'],
    [0.1111111111111111, '#CAA83C'],
    [0.2222222222222222, '#C5AC4A'],
    [0.3333333333333333, '#BFB157'],
    [0.4444444444444444, '#BAB565'],
    [0.5555555555555556, '#B5B972'],
    [0.6666666666666666, '#B0BD7F'],
    [0.7777777777777778, '#ABC18D'],
    [0.8888888888888888, '#A5C69A'],
    [1.0, '#9BCEB5']
]

light_colorway_all = [
    GOLDENROD,
    ROSYBROWN,
    LIGHTGOLDENROD,
    AZURE,
    AQUAMARINE,
    CADETBLUE,
    DARKSLATEGREEN,
    DARKCYAN,
    DARKSLATECYAN,
    DIMGREY,  # Would be Ivory for the dark version.
]
dark_colorway_all = [
    GOLDENROD,
    ROSYBROWN,
    LIGHTGOLDENROD,
    AZURE,
    AQUAMARINE,
    CADETBLUE,
    DARKSLATEGREEN,
    DARKCYAN,
    DARKSLATECYAN,
    IVORY,  # Would be Dimgrey for the light version.
]

# Default Font and  Heading Sizes
HEADING_FONT_1 = 'BebasNeue-Regular'
SUBHEADING_FONT_1 = 'Bebas Neue'
BODY_FONT_1 = 'Montserrat'

TITLE_SIZE = 48
FONT_SIZE = 18
MIN_TXT_SIZE = 16

"""
Use this to assign colors to specific values. A for example could be Sales, and B could be Expenses. Add new entries
as needed. This is only if you know the names of columns ahead of time or feel like hard-coding things.
"""
COLORS_MAPPER = {
    "A": "#38BEC9",
    "B": "#D64545"
}

pio.templates["atbAnalyticsGroupDefaultDark"] = go.layout.Template(
    # ORIG LAYOUT Object
    #
    # {
    #     'annotationdefaults': {'arrowcolor': '#2a3f5f', 'arrowhead': 0, 'arrowwidth': 1},
    #     'autotypenumbers': 'strict',
    #     'coloraxis': {'colorbar': {'outlinewidth': 0, 'ticks': ''}},
    #     'colorscale': {'diverging': [[0, '#8e0152'], [0.1, '#c51b7d'], [0.2,
    #                                  '#de77ae'], [0.3, '#f1b6da'], [0.4, '#fde0ef'],
    #                                  [0.5, '#f7f7f7'], [0.6, '#e6f5d0'], [0.7,
    #                                  '#b8e186'], [0.8, '#7fbc41'], [0.9, '#4d9221'],
    #                                  [1, '#276419']],
    #                    'sequential': [[0.0, '#0d0887'], [0.1111111111111111,
    #                                   '#46039f'], [0.2222222222222222, '#7201a8'],
    #                                   [0.3333333333333333, '#9c179e'],
    #                                   [0.4444444444444444, '#bd3786'],
    #                                   [0.5555555555555556, '#d8576b'],
    #                                   [0.6666666666666666, '#ed7953'],
    #                                   [0.7777777777777778, '#fb9f3a'],
    #                                   [0.8888888888888888, '#fdca26'], [1.0,
    #                                   '#f0f921']],
    #                    'sequentialminus': [[0.0, '#0d0887'], [0.1111111111111111,
    #                                        '#46039f'], [0.2222222222222222, '#7201a8'],
    #                                        [0.3333333333333333, '#9c179e'],
    #                                        [0.4444444444444444, '#bd3786'],
    #                                        [0.5555555555555556, '#d8576b'],
    #                                        [0.6666666666666666, '#ed7953'],
    #                                        [0.7777777777777778, '#fb9f3a'],
    #                                        [0.8888888888888888, '#fdca26'], [1.0,
    #                                        '#f0f921']]},
    #     'colorway': [#636efa, #EF553B, #00cc96, #ab63fa, #FFA15A, #19d3f3, #FF6692,
    #                  #B6E880, #FF97FF, #FECB52],
    #     'font': {'color': '#2a3f5f'},
    #     'geo': {'bgcolor': 'white',
    #             'lakecolor': 'white',
    #             'landcolor': '#E5ECF6',
    #             'showlakes': True,
    #             'showland': True,
    #             'subunitcolor': 'white'},
    #     'hoverlabel': {'align': 'left'},
    #     'hovermode': 'closest',
    #     'mapbox': {'style': 'light'},
    #     'paper_bgcolor': 'white',
    #     'plot_bgcolor': '#E5ECF6',
    #     'polar': {'angularaxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''},
    #               'bgcolor': '#E5ECF6',
    #               'radialaxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''}},
    #     'scene': {'xaxis': {'backgroundcolor': '#E5ECF6',
    #                         'gridcolor': 'white',
    #                         'gridwidth': 2,
    #                         'linecolor': 'white',
    #                         'showbackground': True,
    #                         'ticks': '',
    #                         'zerolinecolor': 'white'},
    #               'yaxis': {'backgroundcolor': '#E5ECF6',
    #                         'gridcolor': 'white',
    #                         'gridwidth': 2,
    #                         'linecolor': 'white',
    #                         'showbackground': True,
    #                         'ticks': '',
    #                         'zerolinecolor': 'white'},
    #               'zaxis': {'backgroundcolor': '#E5ECF6',
    #                         'gridcolor': 'white',
    #                         'gridwidth': 2,
    #                         'linecolor': 'white',
    #                         'showbackground': True,
    #                         'ticks': '',
    #                         'zerolinecolor': 'white'}},
    #     'shapedefaults': {'line': {'color': '#2a3f5f'}},
    #     'ternary': {'aaxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''},
    #                 'baxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''},
    #                 'bgcolor': '#E5ECF6',
    #                 'caxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''}},
    #     'title': {'x': 0.05},
    #     'xaxis': {'automargin': True,
    #               'gridcolor': 'white',
    #               'linecolor': 'white',
    #               'ticks': '',
    #               'title': {'standoff': 15},
    #               'zerolinecolor': 'white',
    #               'zerolinewidth': 2},
    #     'yaxis': {'automargin': True,
    #               'gridcolor': 'white',
    #               'linecolor': 'white',
    #               'ticks': '',
    #               'title': {'standoff': 15},
    #               'zerolinecolor': 'white',
    #               'zerolinewidth': 2}
    # }
    layout={
        # Fonts
        # Note - 'family' must be a single string, NOT a list or dict!
        'title':
            {'font': {
                'family': f'{HEADING_FONT_1}, {SUBHEADING_FONT_1}, Helvetica, Sans-serif',
                'size': TITLE_SIZE,
                'color': IVORY
            },
            },
        'font': {
            'family': f'{BODY_FONT_1}, Helvetica Neue, Helvetica, Sans-serif',
            'size': FONT_SIZE,
            'color': IVORY,
        },
        # Coloring
        'coloraxis': {
            'colorbar': {
                'outlinewidth': 0,
                'ticks': '',
            }
        },
        'colorscale': {
            'diverging': dark_cyan_to_aqua,
            'sequential': cadet_to_aqua_seq,
            'sequentialminus': cadet_to_aqua_seq_min
            # Aquamarine to Rosy Red
            # 'diverging': [
            #     [0, '#9bceb5'],
            #     [0.1, '#a9d2bd'],
            #     [0.2, '#b7d5c6'],
            #     [0.3, '#c5d9ce'],
            #     [0.4, '#d2dcd7'],
            #     [0.5, '#dfdfdf'],
            #     [0.6, '#ddd2d1'],
            #     [0.7, '#dac4c4'],
            #     [0.8, '#d6b6b6'],
            #     [0.9, '#d2a9a8'],
            #     [1, '#ce9b9b']
            # ],

            # Dark Cyan to Aquamarine
            # 'diverging': [
            #     [0, '#1F4F57'],
            #     [0.1, '#2B5C60'],
            #     [0.2, '#38686A'],
            #     [0.3, '#447573'],
            #     [0.4, '#51827D'],
            #     [0.5, '#5D8F86'],
            #     [0.6, '#699B8F'],
            #     [0.7, '#76A899'],
            #     [0.8, '#82B5A2'],
            #     [0.9, '#8FC1AC'],
            #     [1, '#9BCEB5']
            # ],
            # Goldenrod to Aquamarine
            # 'diverging': [
            #     [0, '#CFA42F'],
            #     [0.1, '#CAA83C'],
            #     [0.2, '#C5AC4A'],
            #     [0.3, '#BFB157'],
            #     [0.4, '#BAB565'],
            #     [0.5, '#B5B972'],
            #     [0.6, '#B0BD7F'],
            #     [0.7, '#ABC18D'],
            #     [0.8, '#A5C69A'],
            #     [0.9, '#A0CAA8'],
            #     [1, '#9BCEB5']
            # ],

            # Dark Cyan to Aquamarine
            # 'diverging': [
            #     [0, '#388895'],
            #     [0.1, '#428F98'],
            #     [0.2, '#4C969B'],
            #     [0.3, '#569D9F'],
            #     [0.4, '#60A4A2'],
            #     [0.5, '#6AABA5'],
            #     [0.6, '#73B2A8'],
            #     [0.7, '#7DB9AB'],
            #     [0.8, '#87C0AF'],
            #     [0.9, '#91C7B2'],
            #     [1, '#9BCEB5']
            # ],

            # Cadet Blue to Aquamarine
            # 'sequential': [
            #     [0.0, '#709784'],
            #     [0.1111111111111111, '#749C89'],
            #     [0.2222222222222222, '#79A28E'],
            #     [0.3333333333333333, '#7DA893'],
            #     [0.4444444444444444, '#81AD98'],
            #     [0.5555555555555556, '#86B39D'],
            #     [0.6666666666666666, '#8AB8A1'],
            #     [0.7777777777777778, '#8EBEA6'],
            #     [0.8888888888888888, '#92C3AB'],
            #     [1.0, '#9BCEB5']
            # ],
            #
            # # Cadet Blue to Aquamarine reveresed
            # 'sequentialminus': [
            #     [0.0, '#709784'],
            #     [0.1111111111111111, '#749C89'],
            #     [0.2222222222222222, '#79A28E'],
            #     [0.3333333333333333, '#7DA893'],
            #     [0.4444444444444444, '#81AD98'],
            #     [0.5555555555555556, '#86B39D'],
            #     [0.6666666666666666, '#8AB8A1'],
            #     [0.7777777777777778, '#8EBEA6'],
            #     [0.8888888888888888, '#92C3AB'],
            #     [1.0, '#9BCEB5']
            # ],
        },
        'colorway': dark_colorway_all,

        #     [
        #     GOLDENROD,
        #     ROSYBROWN,
        #     LIGHTGOLDENROD,
        #     AZURE,
        #     AQUAMARINE,
        #     CADETBLUE,
        #     DARKSLATEGREEN,
        #     DARKCYAN,
        #     DARKSLATECYAN,
        #     IVORY,  # Would be Dimgrey for the light version.
        # ],

        # Keep adding others as needed below
        'hovermode': 'x unified',
        'hoverlabel': {
            'align': 'left',
            'bgcolor': DIMGREY,
            'font_size': FONT_SIZE,
            'font_family': BODY_FONT_1
        },
        'hoverdistance': 100,
        'spikedistance': 1000,
        'paper_bgcolor': DIMGREY,
        'plot_bgcolor': DIMGREY,
        'xaxis': {
            'automargin': True,
            'gridcolor': IVORY,
            'linecolor': IVORY,
            'ticks': '',
            'title': {
                'standoff': 15
            },
            'zerolinecolor': IVORY,
            'zerolinewidth': 2,
            'showspikes': True,
            'spikethickness': 2,
            'spikedash': "dot",
            'spikecolor': IVORY,
            'spikemode': "across",

        },
        'yaxis': {
            'automargin': True,
            'gridcolor': DIMGREY,
            'linecolor': IVORY,
            'ticks': '',
            'title': {
                'standoff': 15
            },
            'zerolinecolor': IVORY,
            'zerolinewidth': 2,
            'showspikes': True,
            'spikethickness': 2,
            'spikedash': "dot",
            'spikecolor': IVORY,
            # 'spikemode': "across",
        },
        'uniformtext': {
            # 'minsize': MIN_TXT_SIZE,
            'mode': 'hide',
        },
    },
    # DATA
    data={
        # Each graph object must be in a tuple or list for each trace

        # {
        #     'bar': [{'error_x': {'color': '#2a3f5f'},
        #              'error_y': {'color': '#2a3f5f'},
        #              'marker': {'line': {'color': '#E5ECF6', 'width': 0.5},
        #                         'pattern': {'fillmode': 'overlay', 'size': 10, 'solidity': 0.2}},
        #              'type': 'bar'}],
        #     'barpolar': [{'marker': {'line': {'color': '#E5ECF6', 'width': 0.5},
        #                              'pattern': {'fillmode': 'overlay', 'size': 10, 'solidity': 0.2}},
        #                   'type': 'barpolar'}],
        #     'carpet': [{'aaxis': {'endlinecolor': '#2a3f5f',
        #                           'gridcolor': 'white',
        #                           'linecolor': 'white',
        #                           'minorgridcolor': 'white',
        #                           'startlinecolor': '#2a3f5f'},
        #                 'baxis': {'endlinecolor': '#2a3f5f',
        #                           'gridcolor': 'white',
        #                           'linecolor': 'white',
        #                           'minorgridcolor': 'white',
        #                           'startlinecolor': '#2a3f5f'},
        #                 'type': 'carpet'}],
        #     'choropleth': [{'colorbar': {'outlinewidth': 0, 'ticks': ''}, 'type': 'choropleth'}],
        #     'contour': [{'colorbar': {'outlinewidth': 0, 'ticks': ''},
        #                  'colorscale': [[0.0, '#0d0887'], [0.1111111111111111, '#46039f'],
        #                                 [0.2222222222222222, '#7201a8'],
        #                                 [0.3333333333333333, '#9c179e'],
        #                                 [0.4444444444444444, '#bd3786'],
        #                                 [0.5555555555555556, '#d8576b'],
        #                                 [0.6666666666666666, '#ed7953'],
        #                                 [0.7777777777777778, '#fb9f3a'],
        #                                 [0.8888888888888888, '#fdca26'], [1.0, '#f0f921']],
        #                  'type': 'contour'}],
        #     'contourcarpet': [{'colorbar': {'outlinewidth': 0, 'ticks': ''}, 'type': 'contourcarpet'}],
        'heatmap': [
            {
                'colorbar':
                    {
                        'outlinewidth': 0,
                        'ticks': ''
                    },
                'colorscale': aqua_to_rosy,
                #     [
                #     [0, '#CFA42F'],
                #     [0.1, '#CAA83C'],
                #     [0.2, '#C5AC4A'],
                #     [0.3, '#BFB157'],
                #     [0.4, '#BAB565'],
                #     [0.5, '#B5B972'],
                #     [0.6, '#B0BD7F'],
                #     [0.7, '#ABC18D'],
                #     [0.8, '#A5C69A'],
                #     [0.9, '#A0CAA8'],
                #     [1, '#9BCEB5']
                # ],
                'type': 'heatmap'
            }
        ],
        #     'heatmapgl': [{'colorbar': {'outlinewidth': 0, 'ticks': ''},
        #                    'colorscale': [[0.0, '#0d0887'], [0.1111111111111111,
        #                                   '#46039f'], [0.2222222222222222, '#7201a8'],
        #                                   [0.3333333333333333, '#9c179e'],
        #                                   [0.4444444444444444, '#bd3786'],
        #                                   [0.5555555555555556, '#d8576b'],
        #                                   [0.6666666666666666, '#ed7953'],
        #                                   [0.7777777777777778, '#fb9f3a'],
        #                                   [0.8888888888888888, '#fdca26'], [1.0,
        #                                   '#f0f921']],
        #                    'type': 'heatmapgl'}],
        #     'histogram': [{'marker': {'pattern': {'fillmode': 'overlay', 'size': 10, 'solidity': 0.2}}, 'type': 'histogram'}],
        #     'histogram2d': [{'colorbar': {'outlinewidth': 0, 'ticks': ''},
        #                      'colorscale': [[0.0, '#0d0887'], [0.1111111111111111,
        #                                     '#46039f'], [0.2222222222222222, '#7201a8'],
        #                                     [0.3333333333333333, '#9c179e'],
        #                                     [0.4444444444444444, '#bd3786'],
        #                                     [0.5555555555555556, '#d8576b'],
        #                                     [0.6666666666666666, '#ed7953'],
        #                                     [0.7777777777777778, '#fb9f3a'],
        #                                     [0.8888888888888888, '#fdca26'], [1.0,
        #                                     '#f0f921']],
        #                      'type': 'histogram2d'}],
        #     'histogram2dcontour': [{'colorbar': {'outlinewidth': 0, 'ticks': ''},
        #                             'colorscale': [[0.0, '#0d0887'], [0.1111111111111111,
        #                                            '#46039f'], [0.2222222222222222,
        #                                            '#7201a8'], [0.3333333333333333,
        #                                            '#9c179e'], [0.4444444444444444,
        #                                            '#bd3786'], [0.5555555555555556,
        #                                            '#d8576b'], [0.6666666666666666,
        #                                            '#ed7953'], [0.7777777777777778,
        #                                            '#fb9f3a'], [0.8888888888888888,
        #                                            '#fdca26'], [1.0, '#f0f921']],
        #                             'type': 'histogram2dcontour'}],
        #     'mesh3d': [{'colorbar': {'outlinewidth': 0, 'ticks': ''}, 'type': 'mesh3d'}],
        #     'parcoords': [{'line': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}, 'type': 'parcoords'}],
        #     'pie': [{'automargin': True, 'type': 'pie'}],
        #     'scatter': [{'fillpattern': {'fillmode': 'overlay', 'size': 10, 'solidity': 0.2}, 'type': 'scatter'}],
        #     'scatter3d': [{'line': {'colorbar': {'outlinewidth': 0, 'ticks': ''}},
        #                    'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}},
        #                    'type': 'scatter3d'}],
        #     'scattercarpet': [{'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}, 'type': 'scattercarpet'}],
        #     'scattergeo': [{'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}, 'type': 'scattergeo'}],
        #     'scattergl': [{'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}, 'type': 'scattergl'}],
        #     'scattermapbox': [{'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}, 'type': 'scattermapbox'}],
        #     'scatterpolar': [{'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}, 'type': 'scatterpolar'}],
        #     'scatterpolargl': [{'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}, 'type': 'scatterpolargl'}],
        #     'scatterternary': [{'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}, 'type': 'scatterternary'}],
        #     'surface': [{'colorbar': {'outlinewidth': 0, 'ticks': ''},
        #                  'colorscale': [[0.0, '#0d0887'], [0.1111111111111111, '#46039f'],
        #                                 [0.2222222222222222, '#7201a8'],
        #                                 [0.3333333333333333, '#9c179e'],
        #                                 [0.4444444444444444, '#bd3786'],
        #                                 [0.5555555555555556, '#d8576b'],
        #                                 [0.6666666666666666, '#ed7953'],
        #                                 [0.7777777777777778, '#fb9f3a'],
        #                                 [0.8888888888888888, '#fdca26'], [1.0, '#f0f921']],
        #                  'type': 'surface'}],
        #     'table': [{'cells': {'fill': {'color': '#EBF0F8'}, 'line': {'color': 'white'}},
        #                'header': {'fill': {'color': '#C8D4E3'}, 'line': {'color': 'white'}},
        #                'type': 'table'}]
        # }

        # 'bar': [
        #     go.Bar(
        #         texttemplate='%{value:$.2s}',
        #         textposition='outside',
        #         textfont={
        #             'family': 'Helvetica Neue, Helvetica, Sans-serif',
        #             'size': 20,
        #             'color': BLACK
        #         }
        #     )
        # ],
        # 'line': [
        #     go.Line(
        #
        #     )
        # ],
    }
)
