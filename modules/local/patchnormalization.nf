process PATCHNORMALIZATION{
    
    publishDir "${params.outdir_norm}", mode: 'copy'

    input:
        path patches
        
    output:
        path "**" 

    script:
    """
    Normalize.py \\
        -ip ${patches} \\
        -op ${params.outdir_norm}
    """
    
}