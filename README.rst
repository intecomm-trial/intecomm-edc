|pypi| |actions| |codecov| |downloads|



intecomm-edc
------------


Controlling chronic diseases in Africa: Development and evaluation of an integrated community-based management model for HIV, Diabetes and Hypertension in Tanzania and Uganda (INTE-COMM study)


Liverpool School of Tropical Medicine


http://www.isrctn.com/


See also https://github.com/clinicedc/edc



Installation
------------

To setup and run a test server locally

You'll need mysql and Redis. Create the database

.. code-block:: bash

  mysql -Bse 'create database inte character set utf8;'


Create and activate a virtual environment

.. code-block:: bash

  conda create -n edc python=3.9
  conda activate edc


Clone the main repo and checkout master

.. code-block:: bash

  mkdir ~/app
  cd ~/app
  git clone https://github.com/intecomm-trial/intecomm-edc.git
  cd ~/app/intecomm-edc
  git checkout master


Copy the test environment file

.. code-block:: bash

  cd ~/app/intecomm-edc
  git checkout master
  cp .env-tests .env


Edit the environment file (.env) to include your mysql password in the ``DATABASE_URL``.

.. code-block:: bash

  # look for and update this line
  DATABASE_URL=mysql://user:password@127.0.0.1:3306/intecomm


Continue with the installation

.. code-block:: bash

  cd ~/app/intecomm-edc
  git checkout master
  pip install -U -r requirements.txt
  python manage.py migrate
  python manage.py import_randomization_list
  python manage.py import_holidays


Ensure Redis is running

.. code-block:: bash

  $ redis-cli ping
  PONG


Create a user and start up `runserver`

.. code-block:: bash

  cd ~/app/intecomm-edc
  git checkout master
  python manage.py createsuperuser
  python manage.py runserver


Login::

  localhost:8000


Once logged in, go to you user account and update your group memberships. As a power user add yourself to the following

* ACCOUNT_MANAGER
* ADMINISTRATION
* AE
* AE_REVIEW
* CLINIC
* DATA_MANAGER
* DATA_QUERY
* EVERYONE
* EXPORT
* LAB
* LAB_VIEW
* PHARMACY
* PII
* RANDO
* REVIEW
* SCREENING
* TMG
* UNBLINDING_REQUESTORS
* UNBLINDING_REVIEWERS

.. |pypi| image:: https://img.shields.io/pypi/v/intecomm-edc.svg
    :target: https://pypi.python.org/pypi/intecomm-edc

.. |actions| image:: https://github.com/intecomm-trial/intecomm-edc/workflows/build/badge.svg?branch=develop
  :target: https://github.com/intecomm-trial/intecomm-edc/actions?query=workflow:build

.. |codecov| image:: https://codecov.io/gh/intecomm-trial/intecomm-edc/branch/develop/graph/badge.svg
  :target: https://codecov.io/gh/intecomm-trial/intecomm-edc

.. |downloads| image:: https://pepy.tech/badge/intecomm-edc
   :target: https://pepy.tech/project/intecomm-edc
