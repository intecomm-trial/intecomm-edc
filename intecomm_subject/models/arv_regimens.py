from intecomm_lists.models import ArvRegimens as Base


class ArvRegimens(Base):
    class Meta:
        proxy = True
        verbose_name = "ARV Regimens"
        verbose_name_plural = "ARV Regimens"
