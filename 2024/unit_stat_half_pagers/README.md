This folder contains scripts that were used to generate Unit stat hal pager pdfs.

#### How to generate Pdfs

- First create a `Data` directory and put all the required data in there

- Run the script `data_prep.py`, it will parse the data, compute and save neccesary data in a new folder `Parsed_data`

- Run the script `pdf_gen.py`, this creates the pdfs in a new folder `Pdfs`

#### Script information

**colour_science_2024.py** - This not run directly by user, it contains the colour info for the plots which are imported to the plot scripts

**data_loader.py** - This is not run directly by the user, but used by the scripts to load the neccesary data

**data_prep.py** - Does all the neccesary parsing and computing, all required data should be placed in `Data` folder (this is created by user manually) and all computed data are saved in `Parsed_data` folder (this is created by the script)

**pdf_gen.py** - This script generates the pdfs and saves in the output folder `Pdfs` (created by the script)

**plot_gen.py** - Used by `pdf_gen.py` script to generate the publication and user plots

**unit_pdf_specs.py** - Contains fine tuning styling specs for some units to impore the alignment. This is imported and used in `pdf_gen.py`

**unit_pdf_template.py** - Contains base reportlab doc specification (size, padding, etc) for the pdf. This is imported and used in `pdf_gen.py`
