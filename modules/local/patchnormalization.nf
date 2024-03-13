process PATCHNORMALIZATION{

    label 'process_medium'
    conda '/home/carollo/.conda/envs/histopreprocess/'

    publishDir "${params.outdir}", mode: 'copy'

    input:
        path patches

    output:
        path "normalized_patches/*"

    script:
    """
    normalization.py \\
        -ip ${patches} \\
        -nt ${params.num_threads}
    """

}
