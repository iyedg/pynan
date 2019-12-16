import plotly.express as px
from pandas_flavor import register_dataframe_accessor
import numpy as np
import webcolors
from .utils import types_as_percentage_of_columns
from loguru import logger

RGB_COLORS = np.array(
    [
        np.array(color, dtype=np.uint8)
        for color in [[241, 196, 15], [52, 73, 94], [155, 89, 182], [52, 152, 219]]
    ],
    dtype=np.uint8,
)
HEX_COLORS = [webcolors.rgb_to_hex(color) for color in RGB_COLORS]

KEYS = ["<class 'str'>", "<class 'np.nan'>", "<class 'float'>", "<class 'int'>"]
RGB_COLORS_MAP = dict(zip(KEYS, RGB_COLORS))
HEX_COLORS_MAP = dict(zip(KEYS, HEX_COLORS))


@register_dataframe_accessor("pynan")
class PyNaN:
    def __init__(self, df):
        self._df = df

    def vis_dtypes(self):
        # def vis_dtypes(self, raster=True, bar=False):
        bar_figure = (
            self._df.pipe(types_as_percentage_of_columns)
            .pipe(
                lambda df: px.bar(
                    df,
                    x="variable",
                    y="percent_of_col",
                    color="type",
                    color_discrete_map=HEX_COLORS_MAP,
                )
            )
            .update_layout(dict(bargap=0, plot_bgcolor="white"))
            .update_yaxes(tickformat="%", title="Percent of total rows")
        )
        return bar_figure


from pandas_flavor import register_dataframe_accessor


@register_dataframe_accessor("finance")
class FinanceAccessor:
    """Extra methods for finance dataframes."""

    def __init__(self, df):
        self._df = df

    def get_losses(self):
        # Slice out values less than 1.
        df = self._df
        losses = df[df["gains_and_losses"] < 0]
        return losses
