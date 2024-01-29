from edc_adverse_event.navbars import ae_navbar_item, tmg_navbar_item
from edc_data_manager.navbar_item import dm_navbar_item
from edc_navbar import Navbar, NavbarItem, site_navbars
from edc_review_dashboard.navbars import navbar_item as review_navbar_item

no_url_namespace = False  # True if settings.APP_NAME == "intecomm_dashboard" else False

navbar = Navbar(name="intecomm_dashboard")


navbar.register(
    NavbarItem(
        name="screen_group",
        title="Screen/Group",
        label="Screen/Group",
        fa_icon="fa-user-plus",
        codename="edc_screening.view_screening_listboard",
        url_name="screen_group_url",
        no_url_namespace=no_url_namespace,
    )
)


navbar.register(
    NavbarItem(
        name="subjects",
        title="Subjects",
        label="Subjects",
        fa_icon="fa-user-circle",
        codename="edc_subject_dashboard.view_subject_listboard",
        url_name="subject_listboard_url",
        no_url_namespace=no_url_namespace,
    )
)

navbar.register(review_navbar_item)
navbar.register(tmg_navbar_item)
navbar.register(ae_navbar_item)
navbar.register(dm_navbar_item)

site_navbars.register(navbar)
