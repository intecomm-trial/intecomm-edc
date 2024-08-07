# Generated by Django 5.0.4 on 2024-04-12 13:26

import edc_model_fields.fields.custom_django_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("intecomm_subject", "0167_alter_careseekinga_accompany_num_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="careseekinga",
            name="money_source_main",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                choices=[
                    ("own_savings", "Own saving (e.g. “loose funds”, bank savings)"),
                    (
                        "family_gift",
                        "Money received from family members that does not need to be repaid",
                    ),
                    ("family_loan", "Loan from family member that needs to be repaid"),
                    (
                        "gift_relative",
                        "Money received from relative/neighbour that does not need to be repaid",
                    ),
                    ("loan_relative", "Loan from relative/neighbour that needs to be repaid"),
                    ("loan_money_lender", "Loan from money lender"),
                    ("loan_bank", "Loan from another source eg bank"),
                    ("community", "Self-help community group"),
                    ("national_insurance", "National health insurance"),
                    ("private_insurance", "Private health insurance"),
                    ("community_insurance", "Community health insurance"),
                    ("waiver", "Government waiver"),
                    (
                        "asset_sale",
                        "Sale of assets (property, livestock, jewellery, household goods, etc)",
                    ),
                    ("OTHER", "Other (specify)"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                metadata="FTODSOURCEMAIN1",
                verbose_name="Of the various sources that you have just mentioned, what was the main source of payment?",
            ),
        ),
        migrations.AlterField(
            model_name="careseekingb",
            name="inpatient_money_sources_main",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                choices=[
                    ("own_savings", "Own saving (e.g. “loose funds”, bank savings)"),
                    (
                        "family_gift",
                        "Money received from family members that does not need to be repaid",
                    ),
                    ("family_loan", "Loan from family member that needs to be repaid"),
                    (
                        "gift_relative",
                        "Money received from relative/neighbour that does not need to be repaid",
                    ),
                    ("loan_relative", "Loan from relative/neighbour that needs to be repaid"),
                    ("loan_money_lender", "Loan from money lender"),
                    ("loan_bank", "Loan from another source eg bank"),
                    ("community", "Self-help community group"),
                    ("national_insurance", "National health insurance"),
                    ("private_insurance", "Private health insurance"),
                    ("community_insurance", "Community health insurance"),
                    ("waiver", "Government waiver"),
                    (
                        "asset_sale",
                        "Sale of assets (property, livestock, jewellery, household goods, etc)",
                    ),
                    ("OTHER", "Other (specify)"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                metadata="FINSOURCEMAIN1",
                verbose_name="Of the various sources that you have just mentioned, what was the main source of payment?",
            ),
        ),
        migrations.AlterField(
            model_name="careseekingb",
            name="money_source_main",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                choices=[
                    ("own_savings", "Own saving (e.g. “loose funds”, bank savings)"),
                    (
                        "family_gift",
                        "Money received from family members that does not need to be repaid",
                    ),
                    ("family_loan", "Loan from family member that needs to be repaid"),
                    (
                        "gift_relative",
                        "Money received from relative/neighbour that does not need to be repaid",
                    ),
                    ("loan_relative", "Loan from relative/neighbour that needs to be repaid"),
                    ("loan_money_lender", "Loan from money lender"),
                    ("loan_bank", "Loan from another source eg bank"),
                    ("community", "Self-help community group"),
                    ("national_insurance", "National health insurance"),
                    ("private_insurance", "Private health insurance"),
                    ("community_insurance", "Community health insurance"),
                    ("waiver", "Government waiver"),
                    (
                        "asset_sale",
                        "Sale of assets (property, livestock, jewellery, household goods, etc)",
                    ),
                    ("OTHER", "Other (specify)"),
                    ("N/A", "Not applicable"),
                ],
                max_length=25,
                metadata="FOUTSOURCEMAIN1",
                verbose_name="Of the various sources that you have just mentioned, what was the main source of payment?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekinga",
            name="money_source_main",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                choices=[
                    ("own_savings", "Own saving (e.g. “loose funds”, bank savings)"),
                    (
                        "family_gift",
                        "Money received from family members that does not need to be repaid",
                    ),
                    ("family_loan", "Loan from family member that needs to be repaid"),
                    (
                        "gift_relative",
                        "Money received from relative/neighbour that does not need to be repaid",
                    ),
                    ("loan_relative", "Loan from relative/neighbour that needs to be repaid"),
                    ("loan_money_lender", "Loan from money lender"),
                    ("loan_bank", "Loan from another source eg bank"),
                    ("community", "Self-help community group"),
                    ("national_insurance", "National health insurance"),
                    ("private_insurance", "Private health insurance"),
                    ("community_insurance", "Community health insurance"),
                    ("waiver", "Government waiver"),
                    (
                        "asset_sale",
                        "Sale of assets (property, livestock, jewellery, household goods, etc)",
                    ),
                    ("OTHER", "Other (specify)"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                metadata="FTODSOURCEMAIN1",
                verbose_name="Of the various sources that you have just mentioned, what was the main source of payment?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekingb",
            name="inpatient_money_sources_main",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                choices=[
                    ("own_savings", "Own saving (e.g. “loose funds”, bank savings)"),
                    (
                        "family_gift",
                        "Money received from family members that does not need to be repaid",
                    ),
                    ("family_loan", "Loan from family member that needs to be repaid"),
                    (
                        "gift_relative",
                        "Money received from relative/neighbour that does not need to be repaid",
                    ),
                    ("loan_relative", "Loan from relative/neighbour that needs to be repaid"),
                    ("loan_money_lender", "Loan from money lender"),
                    ("loan_bank", "Loan from another source eg bank"),
                    ("community", "Self-help community group"),
                    ("national_insurance", "National health insurance"),
                    ("private_insurance", "Private health insurance"),
                    ("community_insurance", "Community health insurance"),
                    ("waiver", "Government waiver"),
                    (
                        "asset_sale",
                        "Sale of assets (property, livestock, jewellery, household goods, etc)",
                    ),
                    ("OTHER", "Other (specify)"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                metadata="FINSOURCEMAIN1",
                verbose_name="Of the various sources that you have just mentioned, what was the main source of payment?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcareseekingb",
            name="money_source_main",
            field=edc_model_fields.fields.custom_django_fields.CharField2(
                choices=[
                    ("own_savings", "Own saving (e.g. “loose funds”, bank savings)"),
                    (
                        "family_gift",
                        "Money received from family members that does not need to be repaid",
                    ),
                    ("family_loan", "Loan from family member that needs to be repaid"),
                    (
                        "gift_relative",
                        "Money received from relative/neighbour that does not need to be repaid",
                    ),
                    ("loan_relative", "Loan from relative/neighbour that needs to be repaid"),
                    ("loan_money_lender", "Loan from money lender"),
                    ("loan_bank", "Loan from another source eg bank"),
                    ("community", "Self-help community group"),
                    ("national_insurance", "National health insurance"),
                    ("private_insurance", "Private health insurance"),
                    ("community_insurance", "Community health insurance"),
                    ("waiver", "Government waiver"),
                    (
                        "asset_sale",
                        "Sale of assets (property, livestock, jewellery, household goods, etc)",
                    ),
                    ("OTHER", "Other (specify)"),
                    ("N/A", "Not applicable"),
                ],
                max_length=25,
                metadata="FOUTSOURCEMAIN1",
                verbose_name="Of the various sources that you have just mentioned, what was the main source of payment?",
            ),
        ),
    ]
