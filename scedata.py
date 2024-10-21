import polars as pl
import logging


class SCEData:

    def __init__(self, meter_data):
        self.logger = logging.getLogger(__name__)
        self.meter_data = meter_data

    def to_csv(self, fl=None, drop="delta"):
        self.data.drop(drop).write_csv(fl)
        return self

    def load(self, sort_cols="from"):
        data = [self.load_file(file) for file in self.meter_data]
        before_drop = sum([data.height for data in data])
        self.data = pl.concat(data).unique().sort(sort_cols)
        after_drop = self.data.height
        self.logger.info(f"Dropping {before_drop-after_drop} rows")
        return self

    def load_file(self, fl):
        config = {
            "source": fl,
            "schema": {
                "date": pl.String,
                "usage": pl.String,
                "quality": pl.String,
            },
            "skip_rows": 13,
        }
        self.logger.debug(f"{config=}")

        df = pl.read_csv(**config)
        self.logger.debug(f"{df=}")

        drop, data = df.pipe(self.cleanse, "date", ["from", "to"])
        self.logger.debug(f"{data=}")
        return data

    @staticmethod
    def cleanse(df, col, fields, by="to") -> tuple[pl.DataFrame]:
        df = (
            df.with_columns(pl.col(col).str.split(by).list.to_struct(fields=fields))
            .unnest(col)
            .pipe(SCEData.read_str_date, fields)
            .with_columns(delta=pl.col("to").sub(pl.col("from")))
        )
        null = pl.any_horizontal(pl.col(fields).is_null())
        nulls, not_nulls = df.filter(null), df.filter(~null).cast({"usage": pl.Float32})
        return nulls, not_nulls

    @staticmethod
    def read_str_date(df, col):
        return df.with_columns(
            pl.col(col).str.strip_chars().str.to_datetime("%F %T", strict=False)
        )
