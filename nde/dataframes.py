import pandas as pd
import inspect
import zlib


def hash_str(value):
    return hex(zlib.crc32(str.encode(value)))

def read_csv(path, header=None, names=None, sep=',', parse_dates=False):
    df = pd.read_csv(path, header=header, names=names, sep=sep, parse_dates=parse_dates)
    source_name = hash_str(path)
    column_provenance = {
        column: [f"{source_name}.{column}"] for column in df.columns
    }
    row_provenance_column = f'__lester_provenance_{source_name}'
    df[row_provenance_column] = range(len(df))
    row_provenance_columns = [row_provenance_column]

    return TrackedDataframe(source_name, df, row_provenance_columns, column_provenance)


def join(left_df, right_df, left_on, right_on):
    return left_df.join(right_df, left_on, right_on)


def union(tracked_dataframes):
    result_source_names = [tracked.source_name for tracked in tracked_dataframes]
    result_df = pd.concat([tracked.df for tracked in tracked_dataframes])
    # TODO this currently assumes that the row provenance polynomials have equal structure
    first = tracked_dataframes[0]
    result_row_provenance_columns = first.row_provenance_columns
    result_column_provenance = first.column_provenance
    return TrackedDataframe(result_source_names, result_df, result_row_provenance_columns, result_column_provenance)


def split(tracked_dataframe, fraction):
    from sklearn.model_selection import train_test_split
    first_df, second_df = train_test_split(tracked_dataframe.df, train_size=fraction,
                                           test_size=(1.0 - fraction), shuffle=True)

    first = TrackedDataframe(tracked_dataframe.source_name, first_df, tracked_dataframe.row_provenance_columns,
                             tracked_dataframe.column_provenance)
    second = TrackedDataframe(tracked_dataframe.source_name, second_df, tracked_dataframe.row_provenance_columns,
                              tracked_dataframe.column_provenance)
    return first, second


class TrackedDataframe:

    def __init__(self, source_name, df, row_provenance_columns, column_provenance):
        self.df = df
        self.source_name = source_name
        self.row_provenance_columns = row_provenance_columns
        self.column_provenance = column_provenance

    def __len__(self):
        return len(self.df)

    def join(self, other, left_on, right_on):
        # TODO handle name collisions here
        result_row_provenance_columns = self.row_provenance_columns + other.row_provenance_columns
        result_column_provenance = {**self.column_provenance, **other.column_provenance}
        result_df = self.df.merge(other.df, left_on=left_on, right_on=right_on)
        return TrackedDataframe(self.source_name, result_df, result_row_provenance_columns, result_column_provenance)

    def filter(self, predicate_expression):

        previous_frame = inspect.currentframe().f_back
        previous_previous_frame = previous_frame.f_back

        local_variables = previous_frame.f_locals
        local_variables.update(previous_previous_frame.f_locals)

        global_variables = previous_frame.f_globals
        global_variables.update(previous_previous_frame.f_globals)

        result_row_provenance_columns = self.row_provenance_columns
        result_column_provenance = self.column_provenance
        result_df = self.df.query(predicate_expression,
                                  local_dict=local_variables, global_dict=global_variables)
        return TrackedDataframe(self.source_name, result_df, result_row_provenance_columns, result_column_provenance)

    def __getitem__(self, columns):
        result_row_provenance_columns = self.row_provenance_columns
        result_column_provenance = {column: provenance for column, provenance in self.column_provenance.items()
                                    if column in columns}
        target_columns = columns + self.row_provenance_columns
        result_df = self.df[target_columns]
        return TrackedDataframe(self.source_name, result_df, result_row_provenance_columns, result_column_provenance)

    def rename(self, column_mapping):
        result_row_provenance_columns = self.row_provenance_columns
        result_column_provenance = self.column_provenance.copy()
        for old_column_name, new_column_name in column_mapping.items():
            result_column_provenance[new_column_name] = result_column_provenance[old_column_name]
        for old_column_name in column_mapping.keys():
            del result_column_provenance[old_column_name]

        result_df = self.df.copy(deep=True)
        result_df = result_df.rename(columns=column_mapping)

        return TrackedDataframe(self.source_name, result_df, result_row_provenance_columns, result_column_provenance)

    def project(self, target_column, source_columns, func):
        result_row_provenance_columns = self.row_provenance_columns
        result_column_provenance = self.column_provenance.copy()
        result_column_provenance[target_column] = [f"{self.source_name}.{column}" for column in source_columns]

        target_column_values = []
        for _, row in self.df.iterrows():
            target_column_values.append(func(row[source_columns].item()))

        result_df = self.df.copy(deep=True)
        result_df[target_column] = target_column_values

        return TrackedDataframe(self.source_name, result_df, result_row_provenance_columns, result_column_provenance)

    def flatmap(self, target_column, source_columns, func):
        result_row_provenance_columns = self.row_provenance_columns
        result_column_provenance = self.column_provenance.copy()
        result_column_provenance[target_column] = [f"{self.source_name}.{column}" for column in source_columns]

        target_column_values = []
        for _, row in self.df.iterrows():
            target_column_values.append(func(row[source_columns].item()))

        result_df = self.df.copy(deep=True)
        result_df[target_column] = target_column_values
        result_df = result_df.explode(target_column).reset_index(drop=True)

        return TrackedDataframe(self.source_name, result_df, result_row_provenance_columns, result_column_provenance)
    

    def view_df(self):
        columns_to_view = [column for column in self.df.columns 
                           if column not in self.row_provenance_columns]
        return self.df[columns_to_view]

    def view_provenance(self, source):

        source_hash = hash_str(source)
        provenance_columns = [column for column in self.row_provenance_columns if source_hash in column]

        if len(provenance_columns) == 0:
            raise ValueError(f"Unknown source {source}!")

        return self.df[provenance_columns].values.tolist()
