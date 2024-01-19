## Introduction

**next-preprocesshisto** is a best-practice histopathology analysis pipeline designed to process and extract patches from H&E slides provided as input. The slides will go through a RGB thresholding and edge detection to isolate the tissue before being tessellated into small patches. Subsequently, these patches will be normalized for downstream analysis.

The pipeline is built using [Nextflow](https://www.nextflow.io), a workflow tool to run tasks across multiple compute infrastructures in a very portable manner. The [Nextflow DSL2](https://www.nextflow.io/docs/latest/dsl2.html) implementation of this pipeline uses one container per process which makes it much easier to maintain and update software dependencies.


## Pipeline summary

* **Input:** Read folder with medical images in svs format.
* **Processing:** The first module utilize RGB thresholding and Canny edge detection to isolate the tissue and then to extract patches for further analysis. Furthermore, it performs a check, discarding patches that are almost completely white, i.e., that have a minimal region of tissue, therefore negligible. The second module deals with the normalization of the extracted patches. It is carried out through the Macenko method.
* **Output:** Tissue-relevant patches are saved in folder `patches`. Optionally, the pipeline saves the patches not interested by the tissue, as well as the image reconstruction, in folders `discard` and `reconstruction`, respectively. On the other hand, normalized patches are saved in the folder `normalized_patches`.

## Quick Start

1. Install [`Nextflow`](https://www.nextflow.io/docs/latest/getstarted.html#installation) (`>=22.10.1`)

2. Download the pipeline and clone the repository

   ```bash
   git clone git@github.com:sandrocarollo/next-preprocesshisto.git
   ```

3. Create and activate conda environment

   ```bash
   conda env create -f environment.yml
   conda activate histopreprocess
   ```

4. Run the pipeline

   ```bash
   nextflow run main.nf 
   ```

5. Start running your own analysis!

   Use:
   ```bash
   nextflow run main.nf --input "path/to/data/folder" --canny_values 40 100 --threshold_cutoff 0.9 --patch_size 512 --full_saving false --outdir './results'
   ```
   where in the flag `--input` replace the predefined folder structure containing the svs files. 

   Optionally, you can add the following flags to set your own parameters and adapt the processing to your needs:
   `--canny_values` to set the two limit values for edge detection [ default values: 40 100 ]
   `--threshold_cutoff` to set the threshold value above which the patch is discarded because it is considered almost completely blank [ default value: 0.9 ]
   `--patch_size` to set the size of patches [ default value: 512 ]
   `--full_saving` to choose whether to obtain only the patches interested by the tissue (false) or also the discarded patches and image reconstruction (true) [ default value: false ]
   `--outdir` to set the folder where the pipeline output is to be obtained [ default value: './results' ]


## Acknowledgments

next/preprocesshisto was originally written by Matteo Girotto, Sandro Carollo.

