process TASK{

   

    input:
        path image

    output:


    script:
    """
    histopreprocess.py \\
        --inputimage ${image}
    """
}