process PATCHNORMALIZATION{
    
    publishDir "${params.outdir_norm}", mode: 'copy'

    input:
        path patches
        
    output:
        path "**"

    script:
    """
    normalization.py \\
        -ip ${patches}
    """
    
}