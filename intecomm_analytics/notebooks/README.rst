Environment for notebooks
=========================

From your code folder, e.g. the intecomm-edc git repo, create a conda environment.

Note that during analysis, some code was changed. We bumped edc from the required 1.0.9 to 1.1.2 and edc-analytics went firther ahead to 1.0.2. Installing the higher versions will trigger a pip compatability warning which may be ignored.

.. code-block::

    conda create -n intecomm python=3.12
    conda activate intecomm
    # install as declared in setup.cfg
    pip install -U .
    # bump up
    pip install -U edc==1.1.2, edc-analytics==1.0.2 selenium
