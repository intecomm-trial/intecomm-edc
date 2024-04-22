|pypi| |actions| |codecov| |downloads|

intecomm-edc
------------
Controlling chronic diseases in Africa: Development and evaluation of an integrated community-based management model for HIV, Diabetes and Hypertension in Tanzania and Uganda (INTE-COMM study)

Liverpool School of Tropical Medicine

University College London (UCL)

http://www.isrctn.com/ISRCTN15319595

See also https://github.com/clinicedc/edc

* Django 4.2 / python 3.11
* EDC (see setup.cfg for version)
* We run live and UAT on Ubuntu with nginx/gunicorn/mysql 8.1

Basic install
-------------
.. code-block:: bash

    conda create -n edc python=3.12
    conda activate edc
    git clone https://github.com/intecomm-trial/intecomm-edc.git ~/apps
    cd ~/apps
    pip install -U .
    python manage.py migrate --settings=intecomm_edc.settings.live  # or uat

Randomization
-------------
Groups of patients are randomized to community integrated care (intervention) or facility integrated care (control).

A patient group is represented by the ``PatientGroup`` model. A ``PatientGroup`` model instance contains patients who are represented by ``PatientLog`` model instances.

Before a group is "ready" to randomize:

* the group membership must meet the ratio of HIV, HTN, DM or multi-morbidity patients.
* the group must meet the minimum group size.
* all patients must be screened as eligible and consented

If "ready", the patient group is randomized when the ``PatientGroup`` model instance saves succcessfully
with field ``randomize_now`` set to YES.

Randomization occurs in the signal ``randomize_patient_group_on_post_save``. The signal
leaves most of the work to the class ``RandomizeGroup``. ``RandomizeGroup`` calls it's ``randomize`` method does the following:

* The group is randomized to intervention or control;
* ``PatientGroup`` model instance is allocated a ``group_identifier``;
* Each ``PatientGroup`` model instance in the group is updated with the ``group_identifier``;
* Each ``SubjectConsent`` model instance in the group is updated with the ``group_identifier`` (which triggers another signal associated with the subject consent. This signal puts the subject on schedule);
* Each ``RegisteredSubject`` model instance in the group is updated with the ``group_identifier``;


.. |pypi| image:: https://img.shields.io/pypi/v/intecomm-edc.svg
    :target: https://pypi.python.org/pypi/intecomm-edc

.. |actions| image:: https://github.com/intecomm-trial/intecomm-edc/actions/workflows/build.yml/badge.svg
  :target: https://github.com/intecomm-trial/intecomm-edc/actions/workflows/build.yml

.. |codecov| image:: https://codecov.io/gh/intecomm-trial/intecomm-edc/branch/develop/graph/badge.svg
  :target: https://codecov.io/gh/intecomm-trial/intecomm-edc

.. |downloads| image:: https://pepy.tech/badge/intecomm-edc
   :target: https://pepy.tech/project/intecomm-edc
