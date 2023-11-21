from django.core.management.base import BaseCommand
from apps.funds import models
from django.utils.text import slugify

import json


class Command(BaseCommand):
    help = "Loads up dummy funds and details into the databse"

    def handle(self):
        with open("apps/funds/extractor/details.json", "r") as file:
            grants = json.load(file)

        for grant in grants:
            agency = models.Agency.obejcts.create(
                name=grant["synopsis"]["agencyDetails"]["agencyName"],
                code=grant["synopsis"]["agencyDetails"]["code"],
                seed=grant["synopsis"]["agencyDetails"]["seed"],
            )
            top_agency = models.Agency.objects.create(
                name=grant["synopsis"]["topAgencyDetails"]["agencyName"],
                code=grant["synopsis"]["topAgencyDetails"]["code"],
                seed=grant["synopsis"]["topAgencyDetails"]["seed"],
            )
            applicant_types = models.ApplicantType.objects.bulk_create(
                models.ApplicantType(
                    name=appl_type["description"],
                    slug=slugify(appl_type["description"]),
                )
                for appl_type in grant["synopsis"]["applicantTypes"]
            )
            funding_instruments = models.FundingInstrument.objects.bulk_create(
                models.FundingInstrument(
                    description=instrument["description"],
                    abbrv=instrument["id"],
                    slug=slugify(instrument["description"]),
                )
                for instrument in grant["synopsis"]["fundingInstruments"]
            )
            activity_categories = models.FundingActivityCategory.objects.bulk_create(
                models.FundingActivityCategory(
                    description=category["description"],
                    abbrv=category["id"],
                    slug=slugify(category["description"]),
                )
                for category in grant["synopsis"]["fundingInstruments"]
            )

            synopsis = models.Synopsis.objects.create(
                opportunity_id=grant["synopsis"]["opportunityId"],
                agency_code=grant["synopsis"]["agencyCode"],
                agency_name=grant["synopsis"]["agencyName"],
                agency_phone=grant["synopsis"]["agencyPhone"],
                agency_address_desc=grant["synopsis"]["agencyAddressDesc"],
                agency_detail=agency,
                top_agency_detail=top_agency,
                agency_contact_phone=grant["synopsis"]["agencyContactPhone"],
                agency_contact_name=grant["synopsis"]["agencyContactName"],
                agency_contact_desc=grant["synopsis"]["agencyContactDesc"],
                agency_contact_email=grant["synopsis"]["agencyContactEmail"],
                description=grant["synopsis"]["synopsisDesc"],
                response_date=grant["synopsis"]["responseDate"],
                posting_date=grant["synopsis"]["postingDate"],
                archive_date=grant["synopsis"]["archiveDate"],
                cost_sharing=grant["synopsis"]["costSharing"],
                award_ceiling=grant["synopsis"]["awardCeiling"],
                award_ceiling_formatted=grant["synopsis"]["awardCeilingFormatted"],
                award_floor=grant["synopsis"]["awardFloor"],
                award_floor_formatted=grant["synopsis"]["awardFloorFormatted"],
                applicant_eligibilty_desc=grant["synopsis"]["applicantEligibilityDesc"],
                created_date=grant["synopsis"]["createdDate"],
                updated_date=grant["synopsis"]["lastUpdatedDate"],
            )
            synopsis.applicant_types.add(applicant_types[:])
            synopsis.funding_instruements.add(funding_instruments[:])
            synopsis.funding_activity_categories.add(activity_categories[:])
            synopsis.save()

        self.stdout.write(
            self.style.SUCCESS("Successfully loaded data into the database")
        )
