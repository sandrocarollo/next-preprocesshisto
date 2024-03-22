process PATCHNORMALIZATION{

    label 'process_medium'
    conda '/home/girotto/.conda/envs/histopreprocess/'

    publishDir "${params.outdir}", enabled:params.norm_patches_saving, mode: 'copy'

    input:
        path patches

    output:
        path "normalized_patches/*"

    script:
    """
    normalization.py \
        --inputPath ${patches} \
        --threads ${params.num_threads}

    rm *.jpg
    """

}
