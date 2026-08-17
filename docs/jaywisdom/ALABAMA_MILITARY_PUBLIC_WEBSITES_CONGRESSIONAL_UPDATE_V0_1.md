# Alabama Military Public Websites — Congressional Update v0.1

## Scope

This is a bounded public-reference inventory for congressional replay. It records official public-facing military and National Guard web locators associated with Alabama. It does not collect operational intelligence, prove every statement on a page, create a legal finding, or perform a government submission.

## Public website inventory

| ID | Component | Public surface | Contract state |
|---|---|---|---|
| AL_ARMY_REDSTONE_ARSENAL | U.S. Army | https://home.army.mil/redstone/ | OFFICIAL_PUBLIC_PAGE_VERIFIED |
| AL_ARMY_ANNISTON_ARMY_DEPOT | U.S. Army | https://anad.army.mil/ | OFFICIAL_PUBLIC_PAGE_VERIFIED |
| AL_ARMY_FORT_RUCKER_AVCOE | U.S. Army | https://home.army.mil/rucker/ | OFFICIAL_PUBLIC_PAGE_VERIFIED |
| AL_AIR_FORCE_MAXWELL_GUNTER | U.S. Air Force | https://www.maxwell.af.mil/ | OFFICIAL_PUBLIC_PAGE_VERIFIED |
| AL_ANG_187_FIGHTER_WING | Alabama Air National Guard | https://www.187fw.ang.af.mil/ | OFFICIAL_PUBLIC_PAGE_VERIFIED |
| AL_ANG_117_AIR_REFUELING_WING | Alabama Air National Guard | https://www.117arw.ang.af.mil/ | OFFICIAL_PUBLIC_PAGE_VERIFIED |
| AL_NATIONAL_GUARD_STATE_HOME | Alabama National Guard | https://al.ng.mil/ | OFFICIAL_PUBLIC_PAGE_VERIFIED |
| AL_USCG_ATC_MOBILE | U.S. Coast Guard | https://www.forcecom.uscg.mil/Our-Organization/FORCECOM-UNITS/ATC/ | OFFICIAL_PUBLIC_PAGE_VERIFIED |
| AL_USCG_SECTOR_MOBILE | U.S. Coast Guard | https://www.atlanticarea.uscg.mil/Our-Organization/Heartland-District/Units/Sector-Mobile/ | OFFICIAL_PUBLIC_PAGE_VERIFIED |
| AL_USMCR_MOBILE_BATTLESPACE_SURVEILLANCE_COMPANY | U.S. Marine Corps Forces Reserve | https://www.marforres.marines.mil/Units/Force-Headquarters-Group/Intelligence-Support-Battalion/Battlespace-Surveillance-Company/ | OFFICIAL_PUBLIC_PAGE_VERIFIED |
| AL_NAVY_RESERVE_CENTER_BIRMINGHAM_REFERENCE | U.S. Navy Reserve | https://www.navyreserve.navy.mil/News/Article-View-News/Article/3485801/profiles-in-professionalism-lt-melissa-bagwell-seifert/ | OFFICIAL_REFERENCE_PAGE_VERIFIED_DEDICATED_HOME_NOT_VERIFIED |

## Public-web delta

The Army currently exposes a Fort Rucker garrison surface at `home.army.mil/rucker/`, while an official `army.mil/novosel` surface remains publicly available. The contract records this only as `OFFICIAL_PUBLIC_WEB_NOMENCLATURE_DELTA` and asks whether official installation names, aliases, redirects, and archival labels are synchronized.

```text
WEBSITE_DELTA != ERROR_PROVEN
WEBSITE_DELTA != INTENT_PROVEN
WEBSITE_DELTA != MISCONDUCT
MISSING_DEDICATED_HOME = GAP_NOT_MISCONDUCT
```

## Congressional replay questions

1. Are official Alabama military installation and unit public websites current and consistently named across service-owned domains?
2. Where an official unit is referenced but a dedicated public home is not verified, should the state remain a public-information gap rather than be filled from secondary sources?
3. Do public website changes preserve enough archival/version context for citizens and congressional staff to distinguish current information from stale or transitional pages?
4. Are public affairs and FOIA pathways discoverable from the official public-facing surfaces without treating those pathways as proof of an underlying allegation?

## Execution boundary

```text
PUBLIC_PAGE_LOCATOR_VERIFIED != ALL_PAGE_CONTENT_TRUE
OFFICIAL_DOMAIN != LEGAL_FINDING
TOOL_CALL != GOVERNMENT_ACTION
OPENAI_DEVELOPER_SURFACE != REPOSITORY_EXECUTOR
MODEL_EXECUTION_PERFORMED = FALSE
AUTHORITY_CREATED = FALSE
```

No live congressional submission is performed by this artifact.
