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

    def stepRegisterInit():
        K0 = 300
        alpha = 0.7
        W2 = 3
        TH_pk = 25
        TH_s = 200

        TH = 6
        W1 = 3
        TH_vy = 15

        return K0, alpha, W2, TH_pk, TH_s, TH, W1, TH_vy
