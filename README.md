# Working Families Party - NYC Vote Share

**DISCLAIMER**: I am not a WFP staffer, nor has any of this data been obtained via proprietary channels. 

All data represented in this project is available publicly at the links below:

* [Election Data](https://vote.nyc/page/election-results-summary)
* [District Shapefiles](https://www.nyc.gov/site/planning/data-maps/open-data/districts-download-metadata.page)

## Analysis
WFP vote share was calculated as follows:
* Election data records were filtered down to votes for Kamala Harris
* Harris votes on both party lines - Democratic and WFP - were summed at the elction district level
* WFP vote share was calculated as `WFP votes / All Harris votes` per election district

See [the cleanup script](./src/utils/run_analytics.py) for these steps

The data was mapped using Folium - see [the mapping script](./src/utils/build_map.py)

You can run these steps locally by executing `make map` at the command line

## Source Code
The Folium map is hosted with Flask running in a Docker container. You can build this at any time with `make dev build=true` (and re-run without building with `make dev`)
