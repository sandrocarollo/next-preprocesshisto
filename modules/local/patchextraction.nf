process PATCHEXTRACTION{

    label 'process_high'

    publishDir "${params.outdir}", mode: 'copy'

    conda "/home/girotto/.conda/envs/histopreprocess/"

    input:
        path image

    output:
        path "**"

    script:
    def saving_choosen = params.full_saving ? '--apply_FullSaving' : ''
    """
    histopreprocess.py \\
        --input_image ${image} \\
        --CannyValues ${params.canny_values[0]} ${params.canny_values[1]}\\
        --CleaningThreshold ${params.threshold_cutoff} \\
        --PatchPixelSize ${params.patch_size} \\
        ${saving_choosen}
    """
    
}
