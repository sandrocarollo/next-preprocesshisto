## Introduction

**next-preprocesshisto** is a bioinformatics best-practice analysis pipeline designed to process and extract patches from H&E slides provided as input. The slides will go through a RGB thresholding and edge detection to isoalte the tissue before beign tessellated into small patches for downstream analysis.

The pipeline is built using [Nextflow](https://www.nextflow.io), a workflow tool to run tasks across multiple compute infrastructures in a very portable manner. It uses Docker/Singularity containers making installation trivial and results highly reproducible. The [Nextflow DSL2](https://www.nextflow.io/docs/latest/dsl2.html) implementation of this pipeline uses one container per process which makes it much easier to maintain and update software dependencies. Where possible, these processes have been submitted to and installed from [nf-core/modules](https://github.com/nf-core/modules) in order to make them available to all nf-core pipelines, and to everyone within the Nextflow community!


## Pipeline summary

* **Input:** Read folder with medical images in svs format.
* **Processing:** Utilize RGB thresholding and Canny edge detection to isoalte the tissue and then to extract patches for further analysis. Furthermore, it performs a check, discarding patches that are almost completely white, i.e. that have a minimal region of tissue, therefore negligible.
* **Output:** Patches interested by the tissue are saved in folder `patches`. With the option to additionally save the patches not interested by the tissue and the reconstruction of the image in folders `discard` and `reconstruction` respectively

## Quick Start

1. Install [`Nextflow`](https://www.nextflow.io/docs/latest/getstarted.html#installation) (`>=22.10.1`)

2. Download the pipeline and cloning the repository

   ```bash
   git@github.com:sandrocarollo/next-preprocesshisto.git
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
   nextflow run main.nf --input "path/to/data/folder" 
   ```
   where in the flag `--input` replace the predefined folder structure containing the svs files. 

   In addition, you can add the following flags to set your own parameters and adapt the processing to your needs:
   `--canny_values` to set the two limit values for edge detection [ default values: 40 100 ]
   `--threshold_cutoff` to set the threshold value above which the patch is discarded because it is considered almost completely blank [ default value: 0.9 ]
   `--patch_size` to set the size of patches [ default value: 512 ]
   `--full_saving` to choose whether to obtain only the patches interested by the tissue (false) or also the discarded patches and image reconstruction (true) [ default value: false ]
   `--outdir` to set the folder where the pipeline output is to be obtained [ default value: './results' ]


## Acknowledgments

next/preprocesshisto was originally written by Matteo Girotto, Sandro Carollo.

## Contributions and Support

If you would like to contribute to this pipeline, please see the [contributing guidelines](.github/CONTRIBUTING.md).
