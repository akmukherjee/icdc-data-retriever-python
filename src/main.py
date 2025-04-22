# src/main.py
import asyncio
from fetch_data import (
    get_idc_collections,
    get_tcia_collections,
    get_icdc_study_data,
    get_tcia_collections_data,
)


async def main():
    try:
        # Fetch all required data concurrently
        idc_collections, tcia_collections, icdc_studies = await asyncio.gather(
            get_idc_collections(), get_tcia_collections(), get_icdc_study_data()
        )

        # Get TCIA collections data
        tcia_collections_data = await get_tcia_collections_data(tcia_collections)

        print("Data retrieval completed successfully")
        print(f"Found {len(idc_collections)} IDC collections")
        print(f"Found {len(tcia_collections)} TCIA collections")
        print(f"Found {len(icdc_studies)} ICDC studies")

    except Exception as e:
        print(f"Error in main execution: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
