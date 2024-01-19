process PATCHNORMALIZATION{
    
    label 'process_high'
    conda '/home/girotto/.conda/envs/histopreprocess/'
    
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
