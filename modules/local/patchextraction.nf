process PATCHEXTRACTION{

    label 'process_medium'
    conda "/home/girotto/.conda/envs/histopreprocess/"

    publishDir "${params.outdir}", enabled:params.extr_patches_saving, mode: 'copy'

    input:
        path images

    output:
        path "**"

    script:
    def full_saving_choosen = params.all_extr_patches_saving ? '--apply_FullSaving' : ''
    """
    histopreprocess.py \\
        --input_image ${images} \\
        --CannyValues ${params.canny_values[0]} ${params.canny_values[1]}\\
        --CleaningThreshold ${params.threshold_cutoff} \\
        --PatchPixelSize ${params.patch_size} \\
        ${full_saving_choosen} \\
        --threads ${params.num_threads}  
    """

}
