from config import MANIPULATIONS
from mapping_loader import load_cut_mapping
from runner import run_manipulations


def main():

    mapping_df = (
        load_cut_mapping()
    )

    run_manipulations(
        mapping_df,
        MANIPULATIONS
    )


if __name__ == "__main__":
    main()
