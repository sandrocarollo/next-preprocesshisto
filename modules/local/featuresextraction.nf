process FEATURESEXTRACTION{

    label 'process_medium'
    conda '/home/carollo/.conda/envs/histopreprocess/'

    publishDir "${params.outdir}", mode: 'copy'

    input:
        path norm_patches

    output:
        path "extracted_features/*"

    script:
    """
    python3 ${baseDir}/bin/extract/ctranspath \
        --checkpoint-path ${baseDir}/bin/extract/ctranspath/ctranspath.pth \
        --nt ${params.num_threads} \
        --device ${params.device} \
        ${norm_patches}
    """

}