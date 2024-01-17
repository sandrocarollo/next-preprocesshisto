process PATCHNORMALIZATION{
    
    publishDir "${params.outdir}", mode: 'copy'

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