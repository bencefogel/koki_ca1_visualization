import numpy as np
import pandas as pd
import altair


def get_total_pos(df: pd.DataFrame) -> np.ndarray:
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


if __name__ == '__main__':
    input_dir = 'L:/cluster_seed30/partitioned_data'
    part_neg = pd.read_csv(input_dir + '/partitioned_currents/im_part_neg_0.csv')
    part_pos = pd.read_csv(input_dir + '/partitioned_currents/im_part_pos_0.csv')

    total_pos = get_total_pos(part_pos)
    cnorm_pos = get_cnorm_pos(part_pos)
