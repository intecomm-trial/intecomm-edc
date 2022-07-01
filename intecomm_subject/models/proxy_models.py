from intecomm_lists.models import ArvRegimens as BaseArvRegimens


class ArvRegimens(BaseArvRegimens):
    class Meta:
        verbose_name = "ARV Regimens"
        verbose_name_plural = "ARV Regimens"
        proxy = True
