import os

import pandas as pd
from logger import logger

##########


def build_election_metadata(election_data: pd.DataFrame) -> pd.DataFrame:
    """
    Performs several transformations to the data:
    * Reshapes data to provide valid column headers
    * Adds boolean columns to flag rows of interest
    """

    logger.info("Building election metadata...")

    def build_ed_key(df):
        _ad = str(df["ad"])
        _ed = str(df["ed"])

        if len(_ed) == 1:
            key = f"{_ad}00{_ed}"
        elif len(_ed) == 2:
            key = f"{_ad}0{_ed}"
        elif len(_ed) == 3:
            key = f"{_ad}{_ed}"

        return int(key)

    logger.debug("Resetting headers...")
    _headers = election_data.iloc[0, 0:11]
    _nyc_cleaned = election_data.iloc[:, 11:]
    _nyc_cleaned.columns = [x.lower().replace(" ", "_") for x in _headers]

    # Add in election district key to match to the shapefile
    logger.debug("Adding district key...")
    _nyc_cleaned["ElectDist"] = _nyc_cleaned.apply(lambda x: build_ed_key(x), axis=1)

    # Tag rows as vote tallies
    logger.debug("Adding boolean metadata...")
    _nyc_cleaned["is_vote_total"] = _nyc_cleaned["unit_name"].apply(
        lambda x: "Harris" in x or "Trump" in x
    )
    _nyc_cleaned["is_democratic"] = _nyc_cleaned["unit_name"].apply(
        lambda x: "Harris" in x
    )
    _nyc_cleaned["is_working_families"] = _nyc_cleaned["unit_name"].apply(
        lambda x: "Working Families" in x
    )

    # Get vote tallies in numeric form
    _nyc_cleaned["tally"] = _nyc_cleaned["tally"].apply(
        lambda x: int(x.replace(",", ""))
    )

    return _nyc_cleaned[_nyc_cleaned["is_vote_total"]].reset_index(drop=True)


def build_metrics(election_data: pd.DataFrame) -> pd.DataFrame:
    """
    Performs several analytical steps
    * Filters down to Democratic votes
    * Calculates percentage of Harris votes were cast by WFP voters
    """

    logger.info("Building WFP metrics model...")

    # Get all democratic votes
    logger.debug("Getting democratic vote totals...")
    _harris_votes_by_district = (
        election_data[election_data["is_democratic"]]
        .groupby("ElectDist")
        .agg(vote_totals=("tally", "sum"))
        .reset_index()
    )

    # Get WFP votes
    logger.debug("Getting WFP vote totals...")
    _wfp_votes_by_district = (
        election_data[election_data["is_working_families"]]
        .groupby("ElectDist")
        .agg(wfp_vote_totals=("tally", "sum"))
        .reset_index()
    )

    # Combine the two dataframes above
    logger.debug("Combining dataframes...")
    _wfp_metrics = _wfp_votes_by_district.merge(
        _harris_votes_by_district, on="ElectDist"
    )

    # Calculate percentage of WFP vote share
    logger.debug("Getting WFP vote percentage...")
    _wfp_metrics["wfp_pct"] = (
        100 * _wfp_metrics["wfp_vote_totals"] / _wfp_metrics["vote_totals"]
    )

    _wfp_metrics["wfp_pct"].fillna(0, inplace=True)

    return _wfp_metrics


def main(data_directory: os.path, election_data: pd.DataFrame):
    # Add metadata columns
    election_data__clean = build_election_metadata(election_data=election_data)
    logger.debug(election_data__clean.head())

    # Get election metrics
    election_data__metrics = build_metrics(election_data=election_data__clean)
    logger.debug(election_data__metrics.head())

    # Write resulting file to local
    election_data__metrics.to_csv(
        os.path.join(data_directory, "analytics.csv"), index=False
    )


#####

if __name__ == "__main__":
    DATA_DIRECTORY = os.path.abspath("../raw")
    RAW_ELECTION_DATA = pd.read_csv(
        os.path.join(DATA_DIRECTORY, "election_data.csv"), header=None
    )

    main(
        data_directory=DATA_DIRECTORY,
        election_data=RAW_ELECTION_DATA,
    )
