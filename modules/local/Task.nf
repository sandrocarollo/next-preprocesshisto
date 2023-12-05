process TASK{

    publishDir "${params.outdir}"

    input:
        path image

    output:
        path outputFolder

    script:
    """
    outputFolder=$(python histopreprocess.py --inputimage ${image})

    echo "outputFolder=$outputFolder" > output.info
    """
}