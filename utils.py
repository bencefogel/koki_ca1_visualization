import numpy as np
import pandas as pd
import altair as alt
import altair_saver
from altair import VConcatChart


def get_total_pos(df: pd.DataFrame) -> pd.Series:
    df = df.drop('itype', axis=1)
    assert (df >= 0).all().all()
    return df.sum(axis=0)


def get_total_neg(df: pd.DataFrame) -> pd.Series:
    df = df.drop('itype', axis=1)
    assert (df <= 0).all().all()
    return df.sum(axis=0)


def get_cnorm_pos(df: pd.DataFrame) -> pd.DataFrame:
    total = get_total_pos(df)
    df = df.set_index('itype')
    return df.div(total, axis=1)


def get_cnorm_neg(df: pd.DataFrame) -> pd.DataFrame:
    total = get_total_neg(df)
    df = df.set_index('itype')
    return df.div(total, axis=1)


def create_currsum_pos_chart(df: pd.DataFrame, t: np.ndarray) -> alt.Chart:
    total = get_total_pos(df)
    df_total = pd.DataFrame({'Current': total, 'Time': t})

    currsum_chart = alt.Chart(df_total).mark_area(
        color='black',
        opacity=0.5
    ).encode(
        x=alt.X('Time:Q', title=None, axis=alt.Axis(grid=False, labels=False)),
        y=alt.Y('Current:Q', title='[+nA]')
    ).properties(
        width=1000,
        height=50
    )
    return currsum_chart


def create_currsum_neg_chart(df: pd.DataFrame, t: np.ndarray) -> alt.Chart:
    total = get_total_neg(df)
    df_total = pd.DataFrame({'Current': total, 'Time': t})

    currsum_chart = alt.Chart(df_total).mark_area(
        color='black',
        opacity=0.5
    ).encode(
        x=alt.X('Time:Q', title='Time (ms)', axis=alt.Axis(grid=False)),
        y=alt.Y('Current:Q', title='[-nA]')
    ).properties(
        width=1000,
        height=50
    )
    return currsum_chart


def create_currshares_chart(pos: pd.DataFrame, neg: pd.DataFrame, t: np.ndarray) -> tuple[alt.Chart, alt.Chart]:
    cnorm_pos = get_cnorm_pos(pos)
    cnorm_neg = -1 * get_cnorm_neg(neg)

    custom_color_mapping = {
        'kap': '#51a7f9',
        'kad': '#0365c0',
        'kdr': '#164f86',
        'kslow': '#002452',
        'nad': '#ec5d57',
        'nax': '#c82506',
        'car': '#f39019',
        'passive': '#00882b',
        'capacitive': '#70bf41',
        'AMPA': '#f5d328',
        'NMDA': '#c3971a',
        'GABA': '#b36ae2',
        'GABA_B': '#773f9b',
        'soma_iax_neg': '#a6aaa9',
        'soma_iax_pos': '#a6aaa9'
    }
    # Prepare the dataframes for positive currents
    df_cnorm_pos = pd.DataFrame(cnorm_pos.T)
    df_cnorm_pos['Time'] = t
    df_cnorm_pos_long = df_cnorm_pos.melt(
        id_vars=['Time'],
        var_name='itype',
        value_name='Current'
    )

    # Prepare the dataframes for negative currents
    df_cnorm_neg = pd.DataFrame(cnorm_neg.T)
    df_cnorm_neg['Time'] = t
    df_cnorm_neg_long = df_cnorm_neg.melt(
        id_vars=['Time'],
        var_name='itype',
        value_name='Current'
    )

    # Define custom color scale for the "itype" variable
    color_scale = alt.Scale(domain=list(custom_color_mapping.keys()), range=list(custom_color_mapping.values()))

    # Define the shared y-axis scale
    shared_y_scale = alt.Scale(domain=[-1, 1], padding=0)

    # Create the positive current chart
    currshares_pos_chart = alt.Chart(df_cnorm_pos_long).mark_area().encode(
        x=alt.X('Time:Q', title=None, axis=alt.Axis(grid=False, labels=False)),
        y=alt.Y('Current:Q', stack='zero', scale=shared_y_scale, title="[%]", axis=alt.Axis(grid=False)),
        color=alt.Color('itype:N', scale=color_scale)
    ).properties(
        width=1000,
        height=400
    )

    # Create the negative current chart
    currshares_neg_chart = alt.Chart(df_cnorm_neg_long).mark_area().encode(
        x=alt.X('Time:Q', title=None, axis=alt.Axis(grid=False, labels=False)),
        y=alt.Y('Current:Q', stack='zero', scale=shared_y_scale, axis=alt.Axis(grid=False)),
        color=alt.Color('itype:N', scale=color_scale)
    ).properties(
        width=1000,
        height=400
    )
    return currshares_pos_chart, currshares_neg_chart


def create_vm_chart(v: np.ndarray, t: np.ndarray) -> alt.Chart:
    # Create a DataFrame with the time and potential data
    df = pd.DataFrame({
        'Time': t,
        'Vm': v
    })

    # Create a line chart using Altair
    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('Time:Q', title=None, axis=alt.Axis(grid=False, labels=False)),
        y=alt.Y('Vm:Q', title=None, scale=alt.Scale(domain=[-70, -50]))
    ).properties(
        width=1000,
        height=200
    )
    return chart


def combine_charts(vm: alt.Chart, totalpos: alt.Chart, currshares_pos: alt.Chart, currshares_neg: alt.Chart,
                   totalneg: alt.Chart) -> VConcatChart:
    currshares = alt.layer(
        currshares_pos,
        currshares_neg
    )

    chart = alt.vconcat(totalpos, currshares).properties(
        spacing=0
    )

    chart = alt.vconcat(chart, totalneg).properties(
        spacing=0
    )

    chart = alt.vconcat(vm, chart).properties(
        spacing=0
    )
    return chart


if __name__ == '__main__':
    pass
