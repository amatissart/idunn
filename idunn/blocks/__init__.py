from .opening_hour import OpeningHourBlock
from .phone import PhoneBlock
from .information import InformationBlock
from .website import WebSiteBlock
from .contact import ContactBlock
from .wikipedia import WikipediaBlock
from .services_and_information import ServicesAndInformationBlock, AccessibilityBlock, InternetAccessBlock, BreweryBlock

ALL_BLOCKS = [OpeningHourBlock, PhoneBlock, InformationBlock, WikipediaBlock, WebSiteBlock, ContactBlock, ServicesAndInformationBlock, AccessibilityBlock, InternetAccessBlock, BreweryBlock]
BLOCK_TYPE_TO_CLASS = {b.BLOCK_TYPE: b for b in ALL_BLOCKS}
