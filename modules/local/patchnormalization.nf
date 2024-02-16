process PATCHNORMALIZATION{

    label 'process_high'
    conda '/home/carollo/.conda/envs/histopreprocess/'

    publishDir "${params.outdir}", mode: 'copy'

    input:
        path patches

    output:
        path "**"

    script:
    """
    normalization.py \\
        -ip ${patches} \\
        -nt ${params.num_threads}
    """

}
