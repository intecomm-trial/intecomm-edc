from edc_locator.models import SubjectLocator as BaseModel


class SubjectLocator(BaseModel):
    class Meta:
        proxy = True
        verbose_name = "Subject Locator"
        verbose_name_plural = "Subject Locators"
