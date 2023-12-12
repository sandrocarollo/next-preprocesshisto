process PATCHEXTRACTION{

    publishDir "${params.outdir}", mode: 'copy'
    def chooseFullSavingArg = params.chooseFullSaving ? '--chooseFullSaving' : ''

    input:
        path image

    output:
        path "**" 

    script:
    """
    histopreprocess.py \\
        --inputimage ${image} \\
        --inputCannyValues ${params.CannyValues[0]} ${params.CannyValues[1]}\\
        --inputCleaningThreshold ${params.CleaningThreshold} \\
        --inputPatchPixelSize ${params.PixelSize} \\
        ${chooseFullSavingArg}
    """
    
}