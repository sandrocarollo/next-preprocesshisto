process TASK{

    publishDir "${params.outdir}", mode: 'copy'

    input:
        path image

    output:
        path "**" 

    script:
    """
    histopreprocess.py \\
        --inputimage ${image} 
    """
    
}