process PATCHEXTRACTION{

    publishDir "${params.outdir}", mode: 'copy'
    def saving_choosen = params.full_saving ? '--apply_FullSaving' : ''

    input:
        path image

    output:
        path "**" 

    script:
    """
    histopreprocess.py \\
        --input_image ${image} \\
        --CannyValues ${params.canny_values[0]} ${params.canny_values[1]}\\
        --CleaningThreshold ${params.threshold_cutoff} \\
        --PatchPixelSize ${params.patch_size} \\
        ${saving_choosen}
    """
    
}