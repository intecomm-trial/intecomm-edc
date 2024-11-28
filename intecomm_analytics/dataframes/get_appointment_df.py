import pandas as pd
from django_pandas.io import read_frame
from edc_appointment.models import Appointment, AppointmentType


def get_appointment_df() -> pd.DataFrame:
    df_appt = read_frame(Appointment.objects.all(), verbose=False)
    df1 = read_frame(AppointmentType.objects.values("id", "name").all())
    df1 = df1.rename(columns={"id": "appt_type"})
    df_appt = df_appt.merge(df1, on="appt_type", how="left")
    df_appt = df_appt.drop(columns=["appt_type"])
    df_appt = df_appt.rename(columns={"name": "appt_type"})
    return df_appt
