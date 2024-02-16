process PATCHEXTRACTION{

    label 'process_high'
    conda "/home/carollo/.conda/envs/histopreprocess/"

    publishDir "${params.outdir}", mode: 'copy'

    input:
        path images

    output:
        path "**"

    script:
    def saving_choosen = params.full_saving ? '--apply_FullSaving' : ''
    """
    histopreprocess.py \\
        --input_image ${images} \\
        --CannyValues ${params.canny_values[0]} ${params.canny_values[1]}\\
        --CleaningThreshold ${params.threshold_cutoff} \\
        --PatchPixelSize ${params.patch_size} \\
        ${saving_choosen} \\
        --threads ${params.num_threads}
    """

}
