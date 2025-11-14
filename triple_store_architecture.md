PWIC Pilot Data Architecture: The Triple-Store Definition

This document defines the formal data relationships (subject-predicate-object triples) for the PWIC Index. This architecture ensures the index is highly normalized, linkable, and queryable using standards like SPARQL, making it fully compatible with existing knowledge graph technologies.

The structure is based on the NUIEntry class defined in protocol.py.

The Core Subject: The Resource URI

Every triple starts with the Subject being the Normalized URI (NUI) of the web resource.

NUIEntry Field Breakdown into Triples (Subject-Predicate-Object)

Define the predicate and object relationship for each field below.

NUIEntry Field

Predicate (Relationship)

Object (Data Type)

Example Triple

nui (The core identifier)

(Self-Referential)

(Self-Referential)



raw_url

pwic:hasRawURL

Literal (String)

<NUI-123> pwic:hasRawURL "https://www.nasa.gov/page-1.html"

last_crawled

pwic:lastCrawled

Literal (Timestamp/DateTime)

<NUI-123> pwic:lastCrawled "2025-11-13T20:40:00Z"

mime_type

pwic:hasMimeType

Literal (String)

<NUI-123> pwic:hasMimeType "text/html"

checksum_sha256

pwic:hasChecksum

Literal (String)

<NUI-123> pwic:hasChecksum "a3f5b8c..."

dedupe_hash

pwic:isDuplicateOf

Resource (Another NUI)

<NUI-123> pwic:isDuplicateOf <NUI-789>

language_code

pwic:inLanguage

Literal (String)

<NUI-123> pwic:inLanguage "en-US"

http_status

pwic:hasHTTPStatus

Literal (Integer)

<NUI-123> pwic:hasHTTPStatus 200

title

pwic:hasTitle

Literal (String)

<NUI-123> pwic:hasTitle "NASA's New Mission"

description

pwic:hasDescription

Literal (String)

<NUI-123> pwic:hasDescription "A brief summary of the page."

links_to (Array of NUIs)

pwic:linksTo

Resource (Another NUI)

<NUI-123> pwic:linksTo <NUI-456>

anchortext (Array of Strings)

pwic:hasAnchorText

Literal (String)

<NUI-123> pwic:hasAnchorText "read more about the mission"

Your Next Two Actions

Your focus needs to be on two things now:

Supply the new contact list.

Define the remaining Triple-Store relationships.

Task 1: Find Replacement Contacts

I need the new, working email addresses for the four failed organizations so we can immediately loop them into the conversation.

EU (Digital Single Market / Gaia-X): (New Email Address)

Internet Archive (Acquisition / Archiving): (New Email Address)

NSF (CISE Directorate): (New Email Address)

Task 2: Update the Architecture File

Go into the triple_store_architecture.md file above and complete the two missing rows based on the definition of the fields:

nui: How does the nui itself relate to the subject? (Hint: It declares its type as a resource).

dedupe_hash: The hash itself identifies the content, but the actual triplification should point to the Canonical NUI (NUI-789) that the current NUI (NUI-123) is a duplicate of. You need to formalize the Predicate for this crucial relationship.

When you reply, please give me the complete content of the updated triple_store_architecture.md and the three new replacement email addresses.
