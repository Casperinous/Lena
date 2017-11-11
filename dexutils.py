from items import MapItem
from androguard.core.bytecodes.dvm import MapList
class DexUtils:

    @staticmethod
    def groupMapSections(dex):

        items = []
        for section in dex.getSectionArr():
            if not isinstance(section, MapList):
                arr = section.getRawData()
                item = None
                if isinstance(arr, list):

                    size = len(arr)
                    item = MapItem(section.getTypeId(),section, arr[0], arr[-1], size)
                else:

                    item = MapItem(section.getTypeId(),section, arr, arr, 1)
                items.append(item)
        return items