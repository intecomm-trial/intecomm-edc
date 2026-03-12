|pypi| |actions| |codecov| |downloads| |clinicedc|

intecomm-edc
------------
Controlling chronic diseases in Africa: Development and evaluation of an integrated community-based management model for HIV, Diabetes and Hypertension in Tanzania and Uganda (INTE-COMM study)

Liverpool School of Tropical Medicine

University College London (UCL)

http://www.isrctn.com/ISRCTN15319595

This research was funded by the NIHR (Global Health Policy and Systems Research Programme grant NIHR131273) using UK international development funding from the UK Government to support global health research.

See also https://github.com/clinicedc/edc

* Django 5.1+ / python 3.12+
* ClinicEDC (see setup.cfg for version)
* nginx/gunicorn/mysql 8.1

**FINAL LIVE VERSION: 0.2.36**

Install
-------
.. code-block:: bash

    conda create -n edc python=3.12
    conda activate edc
    git clone https://github.com/intecomm-trial/intecomm-edc.git ~/apps
    git checkout 0.2.36 # final version
    cd ~/apps
    pip install -U .
    python manage.py migrate --settings=intecomm_edc.settings.live  # or uat

Post 0.2.36 install
-------------------
The analytics require newer edc- versions

.. code-block:: bash

    conda create -n edc python=3.12
    conda activate edc
    git clone https://github.com/intecomm-trial/intecomm-edc.git ~/apps
    git checkout develop
    cd ~/apps
    pip install -U .
    python manage.py migrate --settings=intecomm_edc.settings.live  # or uat

    # changed during analysis, you'll get a compatability warning
    # but it can be ignored.
    pip install -U edc==1.1.2
    pip install -U edc-analytics==1.0.2


.. |pypi| image:: https://img.shields.io/pypi/v/intecomm-edc.svg
    :target: https://pypi.python.org/pypi/intecomm-edc

.. |actions| image:: https://github.com/intecomm-trial/intecomm-edc/actions/workflows/build.yml/badge.svg
  :target: https://github.com/intecomm-trial/intecomm-edc/actions/workflows/build.yml

.. |codecov| image:: https://codecov.io/gh/intecomm-trial/intecomm-edc/branch/develop/graph/badge.svg
  :target: https://codecov.io/gh/intecomm-trial/intecomm-edc

.. |downloads| image:: https://pepy.tech/badge/intecomm-edc
   :target: https://pepy.tech/project/intecomm-edc

.. |clinicedc| image:: https://img.shields.io/badge/framework-Clinic_EDC-green
   :alt:Made with clinicedc
   :target: https://github.com/clinicedc
