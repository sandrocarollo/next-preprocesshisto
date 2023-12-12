process PATCHEXTRACTION{

    publishDir "${params.outdir}", mode: 'copy'
    def saving_choosen = params.full_saving ? '--choose_FullSaving' : ''

    input:
        path image

    output:
        path "**" 

    script:
    """
    histopreprocess.py \\
        --input_image ${image} \\
        --input_CannyValues ${params.canny_values[0]} ${params.canny_values[1]}\\
        --input_CleaningThreshold ${params.threshold_cutoff} \\
        --input_PatchPixelSize ${params.patch_size} \\
        ${saving_choosen}
    """
    
}