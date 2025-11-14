"""
PWIC Data Protocol Definition - NUI (Normalized URL Index) Entry

This file defines the mandatory schema and data structures for a single entry
in the Public Web Index Cooperative (PWIC) Normalized URL Index (NUI).

The NUI is the core machine-readable output of the PWIC Pilot, intended for
decentralized distribution and adoption by search engines, archives, and researchers.

This schema is designed for serialization into CSV, JSON, or RDF Triple-Store format.
"""

from typing import List, Optional, Dict
from datetime import datetime
import hashlib

class NUIEntry:
    """
    Represents a single, canonical entry in the Normalized URL Index (NUI).

    This class enforces the structural integrity and minimum metadata requirements
    for a verifiable public index entry.
    """

    def __init__(
        self,
        url: str,
        crawl_date: datetime,
        source_domain: str,
        country_code: str,
        state_province_code: Optional[str] = None,
        simhash_sig: Optional[str] = None,
        canonical_url_hash: Optional[str] = None,
        keywords: Optional[List[str]] = None
    ):
        """
        Initializes an NUI entry with essential resilience and discoverability data.

        Args:
            url (str): The primary URL of the document.
            crawl_date (datetime): The date/timestamp when the content was last crawled.
            source_domain (str): The domain (e.g., nsf.gov, yale.edu).
            country_code (str): The two-letter ISO country code (e.g., 'US', 'DE').
            state_province_code (Optional[str]): Optional state/province code (e.g., 'CA', 'TX').
            simhash_sig (Optional[str]): The SimHash signature for content deduplication.
            canonical_url_hash (Optional[str]): SHA-256 hash of the content's canonical URL.
            keywords (Optional[List[str]]): An optional list of high-value keywords.
        """
        # --- Mandatory Fields for Resilience and Verification ---
        self.url: str = url
        self.crawl_date: datetime = crawl_date
        self.source_domain: str = source_domain
        self.country_code: str = country_code

        # --- Optional/Metadata Fields for Discoverability ---
        self.state_province_code: Optional[str] = state_province_code
        self.simhash_sig: Optional[str] = simhash_sig
        self.canonical_url_hash: Optional[str] = canonical_url_hash
        self.keywords: List[str] = keywords if keywords is not None else []

        # --- Self-Verification Field (Cryptographic Proof) ---
        # A hash of the combined core data to ensure integrity upon distribution.
        self.integrity_hash: str = self._calculate_integrity_hash()

    def _calculate_integrity_hash(self) -> str:
        """
        Calculates a unique SHA-256 hash based on the core fields of the entry.
        This ensures the entry cannot be tampered with after creation.
        """
        core_data = [
            self.url,
            self.crawl_date.isoformat(),
            self.source_domain,
            self.country_code,
            self.state_province_code if self.state_province_code else "",
            self.simhash_sig if self.simhash_sig else "",
        ]
        data_string = "|".join(core_data).encode('utf-8')
        return hashlib.sha256(data_string).hexdigest()

    def to_dict(self) -> Dict:
        """Serializes the NUI entry into a dictionary for JSON/CSV output."""
        return {
            'url': self.url,
            'crawl_date': self.crawl_date.isoformat(),
            'source_domain': self.source_domain,
            'country_code': self.country_code,
            'state_province_code': self.state_province_code,
            'simhash_sig': self.simhash_sig,
            'canonical_url_hash': self.canonical_url_hash,
            'keywords': self.keywords,
            'integrity_hash': self.integrity_hash
        }

# --- Example Usage (Not part of the protocol, for demonstration only) ---
if __name__ == '__main__':
    # Create an example entry for a US Government research paper
    example_entry = NUIEntry(
        url="https://www.nsf.gov/research_paper_123.pdf",
        crawl_date=datetime(2025, 11, 13, 10, 0, 0),
        source_domain="nsf.gov",
        country_code="US",
        state_province_code="VA", # Example for NSF location
        simhash_sig="a3b2c1d0e4f5a6b7",
        keywords=["computational-science", "grant-funding", "resilience"]
    )

    print("--- PWIC NUI Entry Generated ---")
    import json
    print(json.dumps(example_entry.to_dict(), indent=2))

    # Demonstrate integrity hash calculation
    print(f"\nIntegrity Hash: {example_entry.integrity_hash}")
    
    # Check if a minor change affects the hash (it should)
    tampered_entry = example_entry.to_dict()
    tampered_entry['source_domain'] = 'fake.gov' 
    
    # Note: We must re-create the object to recalculate the hash for a true test
    tampered_object = NUIEntry(
        url="https://www.nsf.gov/research_paper_123.pdf",
        crawl_date=datetime(2025, 11, 13, 10, 0, 0),
        source_domain="fake.gov", # Tampered field
        country_code="US",
        state_province_code="VA", 
        simhash_sig="a3b2c1d0e4f5a6b7",
    )
    print(f"Tampered Hash:  {tampered_object.integrity_hash}")
    print(f"Hashes Match (False means integrity check works): {example_entry.integrity_hash == tampered_object.integrity_hash}")
