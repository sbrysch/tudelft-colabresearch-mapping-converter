# Custom data processing

The initial source data has been provided by the Co-Lab Research team in the form of [Excel files](./data/input).



## Conversion algorithms

The conversion algorithms have been built according to the provided specifications: [2021-06-10_FINAL_Categorization_system.pdf](./doc/2021-06-10_FINAL_Categorization_system.pdf) ([updated version- 2021-06-15](./doc/2021-06-15_FINAL_Categorization_system.pdf))

1. [Denmark](doc/dk.md)
2. [Sweden - completed](doc/se_completed.md)
3. [Sweden - wip](doc/se_wip.md)
4. [United Kingdom - England](doc/uk_england.md)



## Usage


### A. Country source files

The [countries source files](./data/input) of this repository are already prepared according to the following process:

- **Sweden**

    1. Open the ``Database CH Sweden 2020.xlsx`` file.
    2. Format the file:
    1. Remove empty rows that are not at the end of the dataset.
    2. Remove all sum rows.
    3. In the cells A1 write `id`.
    4. Complete cells with missing values for `City`: a value is often written to a single cell but its reach to multiple cells implied by the borders.
    5. Search and replace: `condiminium` -> `condominium`
    6. Fix invalid values (e.g.: question mark in year value).
    3. Save the formatted file to ``./data/input/Database CH Sweden 2020 - formatted.xlsx``
    4. Save the _Database CH Sweden 2020_ sheet as `./data/input/sweden-projects-completed.csv` (CSV UTF-8).
    5. Save the _Groups planning new houses_ sheet as `./data/input/sweden-projects-wip.csv` (CSV UTF-8).
    6. Open the file with a text editor and change the delimiter from `,` to `|` (https://onlinecsvtools.com/change-csv-delimiter).

- **Denmark**

    1. Open `Database CH Denmark 2019.xlsx` file.
    2. Format the file:
    1. Remove empty column in the middle of the dataset.
    2. Remove all line breaks in cells.
    3. Remove leading spaces in the cells of `Type of ownership` column.
    3. Save the formatted file to ``./data/input/Database CH Denmark 2019 - formatted.xlsx``
    4. Save again as `./data/input/denmark-projects.csv` (CSV UTF-8).
    5. Open the file with a text editor and change the delimiter from `,` to `|` (https://onlinecsvtools.com/change-csv-delimiter).

- **England**

    1. Open `ENGLAND CLT project data-2020-11-18-10-51-57.xlsx` file.
    2. Format the file:
        1. Remove the first row containing meta titles.
        2. Remove the sum and footer rows.
    3. Save the formatted file to `./data/input/ENGLAND CLT project data-2020-11-18-10-51-57 - formatted.xlsx`
    4. Save again as `./data/input/england-projects.csv` (CSV UTF-8).
    5. Open the file with a text editor and change the delimiter from `,` to `|` (https://onlinecsvtools.com/change-csv-delimiter).


### B. Classifications

All the classification data (taxonomy, definitions, countries descriptions) can be modified by editing the [classification source files](./classification).


### C. Run the converter

After any modification of the source or the classification files, the converter must be executed:

1. Run `python converter.py`.
2. The output files are created in [./data/output](./data/output):
   - `yyyy-mm-dd-hh-mm-ss_aggregated_data.csv`
   - `yyyy-mm-dd-hh-mm-ss_aggregated_data.json`
   - `classification.json`
   - `taxonomy.json`
   - `taxonomy-structured.json`
3. Use of the results:
   - JSON files can be pushed to the [tudelft-colabresearch-mapping-data](https://github.com/odqo/tudelft-colabresearch-mapping-data) repository (see the related readme).
   - `./data/output/co-lab-research-db.sqlite3` can be open with an adapted SQLite client.
   - We can also use _Excel_ to see and work with the data of the `yyyy-mm-dd-hh-mm-ss_aggregated_data.csv` file:
     1. Open _Excel_.
     2. In the _Data_ tab click _From Text/CSV_, choose the exported CSV file and confirm.
     3. In the _Text Import Wizard_ choose the following options:
        - `Delimited`
        - `My data has headers`
        - Delimiters `Other`: `|`
     4. Click _Finish_.
     5. Click the A1 cell, then in the _Insert_ tab click _Table_ and confirm.
     6. Finally we have an _Excel_ with working filters.
     7. You can save the file with _Save As_, choose the `Excel Workbook (*.xlsx)` format.