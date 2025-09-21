.PHONY: all fetch analyze clean

all: analyze

fetch:
	echo "Fetching METAR data for airports..."
	./fetch_metars.sh
	echo "Fetch complete. Raw data saved in raw_metars"

analyze: fetch
	echo "Analyzing METAR data..."
	./analyze_data.sh
	echo "Analysis complete. Results saved in weather_report.csv"

clean:
	echo "Cleaning up generated files..."
	rm -rf raw_metars weather_report.csv
	echo "Cleanup complete."
