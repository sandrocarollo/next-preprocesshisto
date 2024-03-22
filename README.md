## Introduction

**next-preprocesshisto** is a best-practice histopathology analysis pipeline designed to process and extract patches from H&E slides provided as input. The slides will go through a RGB thresholding and edge detection to isolate the tissue before being tessellated into small patches. Subsequently, these patches will be normalized before performing feature extraction via CTransPath.

The pipeline is built using [Nextflow](https://www.nextflow.io), a workflow tool to run tasks across multiple compute infrastructures in a very portable manner. The [Nextflow DSL2](https://www.nextflow.io/docs/latest/dsl2.html) implementation of this pipeline uses one container per process which makes it much easier to maintain and update software dependencies.


## Pipeline summary

* **Input:** Read folder with medical images (Where the following formats are allowed: svs,qptiff,tif,dcm,vms,vmu,ndpi,scn,mrxs,tiff,svslide and bif).
* **Processing:** The first module utilize RGB thresholding and Canny edge detection to isolate the tissue and then to extract patches for further analysis. Furthermore, it performs a check, discarding patches that are almost completely white, i.e., that have a minimal region of tissue, therefore negligible. The second module deals with the normalization of the extracted patches. It is carried out through the Macenko method. The third and final module performs feature extraction using CTransPath.
* **Output:** The extracted features for each slide. Optionally and separately, the pipeline saves the tissue-relevant patches in folder `tiles`, the patches not interested by the tissue, as well as the image reconstruction, in folders `discard` and `reconstruction`, respectively, and the normalized patches, saved in the folder `normalized_patches`.

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
   nextflow run main.nf \
      --input "path/to/data/folder" \
      --canny_values 40 100 \
      --threshold_cutoff 0.9 \
      --patch_size 224 \
      --extr_patches_saving false \
      --all_extr_patches_saving false \
      --norm_patches_saving false \
      --num_threads 10 \
      --outdir 'path/to/outdir'
   ```
   where in the flag `--input` replace the predefined folder structure containing the input files. And `--outdir` replace the predefined folder structure where to save the extracted features and any other optional saves.

   Optionally, you can add the following flags to set your own parameters and adapt the processing to your needs:
   `--canny_values` to set the two limit values for edge detection [ default values: 40 100 ]
   `--threshold_cutoff` to set the threshold value above which the patch is discarded because it is considered almost completely blank [ default value: 0.9 ]
   `--patch_size` to set the size of patches [ default value: 512 ]
   `--extr_patches_saving` to save in the outdir the extracted patches interested by the tissue (true) [ default value: false ]
   `--all_extr_patches_saving` to save in the outdir, in addition to the extracted patches interested by the tissue, also the discarded patches and image reconstruction (true) [ default value: false ]
   `--full_saving` to save in the outdir the normalized patches (true) [ default value: false ]
   `--outdir` to set the folder where the pipeline output is to be obtained [ default value: './results' ]


## Acknowledgments

next-preprocesshisto was originally written by Matteo Girotto, Sandro Carollo.

