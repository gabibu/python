import argparse
import pandas as pd


def _build_codes_stat(input_file: str, output_file: str):
    codes_df = pd.read_csv(input_file)

    code_to_count_df = codes_df.groupby(['code']).size().to_frame('size').reset_index()
    code_to_count_df['weight'] = code_to_count_df['size'] / len(codes_df)

    code_to_count_df[['code', 'weight']].to_csv(output_file, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='build_codes_stat')
    parser.add_argument('--input_file', type=str, required=True)
    parser.add_argument('--output_file', type=str, required=True)
    args = parser.parse_args()

    _build_codes_stat(args.input_file, args.output_file)

    print('1')
