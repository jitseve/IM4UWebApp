class Settings(object):
    """
    =NOTES=
    """

    # Readout settings
    folderpath = 'uploads'
    filetype = 'csv'
    subfolders = False

    # Plot settings
    padding = 5
    savepath = '../figures'

    # Physical settings
    gravity = 9.81
    alpha = 0.85

    # GCT settings
    sw_width = 20  # sliding window width
    sw_type = 'x'

    # IMU settings
    f_sampling = 1/218
