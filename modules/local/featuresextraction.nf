process FEATURESEXTRACTION{

    label 'process_high'
    conda '/home/carollo/.conda/envs/histopreprocess/'

    publishDir "${params.outdir}", mode: 'copy'

    input:
        path norm_patches

    output:
        path "**"

    script:
    """
    python3 ${baseDir}/bin/extract/ctranspath \
        --checkpoint-path ${baseDir}/bin/extract/ctranspath/ctranspath.pth \
        ${norm_patches}
    """

}