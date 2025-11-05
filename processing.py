#! /usr/bin/env python3


if __name__ == "__main__":
    from pathlib import Path
    import pandas as pd

    from sonde import Sonde
    import config

    field_book_fpath = Path(config.field_book_fpath)
    if not field_book_fpath.exists():
        raise FileNotFoundError(f"Field book file is not found: {field_book_fpath}")

    fbook_df = pd.read_csv(field_book_fpath)
    print(fbook_df)

    for _, row in fbook_df.iterrows():
        sonde_no = str(row["sonde_no"])
        st_name = str(row["st_name"])
        launch_time = pd.to_datetime(row["JSTtime"], format="%Y-%m-%d_%H:%M")
        launch_timeUTC = launch_time - pd.Timedelta(hours=9)

        qc_data_fpath = Path(config.qc_data_dir) / f"{sonde_no}_qc.csv"

        s = Sonde(
            sonde_no=sonde_no,
            launch_time=launch_timeUTC,
            raw_data_dir=Path(config.raw_data_dir),
        )
        s.qc_data(qc_data_fpath, recalc=True)

        print(s)
