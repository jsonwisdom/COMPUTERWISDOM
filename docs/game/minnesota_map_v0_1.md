# Minnesota Map v0.1

Author: Jay Wisdom  
Leaf: LEAF_003_PUBLIC_MEMORY_DRIFT_OBSERVATORY_V0_1  
Game: Public Receipt Arcade / Game of Growth  
Map: Minnesota  
Status: Draft  
Authority: false  
Fraud status: UNKNOWN

## Purpose

Define Minnesota as the first playable map for Public Receipt Arcade.

The map is not GIS software.

It is a SNES-style overworld that lives inside an arcade cabinet.

Same ten cabinets. Same joystick travel. Same fog of war. The safety pass swaps debate for documents.

Every starter quest is:

```text
old public file -> new public file -> receipt
```

No opinions.  
No names shown.  
No fraud declaration.  
No authority claim.

## Map Style

Minnesota appears as a chunky 8-bit state tilted like a game controller.

Lakes are blue sparkle tiles.

Highways are glowing dotted lines, not real roads.

The map combines:

- Pokemon region: counties are hidden at first; towns appear first
- Zelda overworld: joystick walking lifts fog
- Arcade row: each town is a standing cabinet with marquee art

No latitude/longitude.
No parcel zoom.
No GIS panel.

Players see icons:

- loon for Saint Cloud
- bridge for Minneapolis
- dome for St Paul
- ore boat for Duluth
- heartbeat for Rochester
- flood gauge for Moorhead
- axe for Bemidji
- bobber for Brainerd
- mine cart for Hibbing
- corn for Mankato

If a receipt about a place passes the Three Courts, that place gets sharper pixels.

## Starter Row

Saint Cloud is home base.

The other nine locations are the starter arcade row.

Players can walk to them with the joystick.

Each cabinet shows only three numbers:

- receipts verified here
- replays done here
- corrections made here

No followers.  
No likes.  
No outrage score.

## 1. Saint Cloud — Home Base

Cabinet: Loon Cabinet

Quest:

```text
Did the parks maintenance budget line move?
```

Source type:

```text
City of Saint Cloud Adopted Budget PDFs, FY2014 and FY2024
```

Receipt generated:

```text
side-by-side crop of line 101-452 Parks Maintenance, with file hash
```

Art / reward unlocks:

- Loon Ledger Quarter
- Parks Pinball Decal

## 2. Minneapolis — Stone Arch

Cabinet: Bridge Cabinet

Quest:

```text
Did posted Stone Arch Bridge hours change?
```

Source type:

```text
Minneapolis Park and Recreation Board meeting packets, 2010-06-02 and 2023-06-07 PDFs
```

Receipt generated:

```text
hours table from each packet, page-paired
```

Art / reward unlocks:

- Bridge Clock Sticker

## 3. St Paul — Capitol Steps

Cabinet: Dome Cabinet

Quest:

```text
Did the state meeting room rental fee change?
```

Source type:

```text
Minnesota Dept. of Administration Facility Use Fee Schedule PDFs, 2015 and 2024
```

Receipt generated:

```text
fee table for Room 316, old vs new
```

Art / reward unlocks:

- Dome Docket Quarter

## 4. Duluth — Lake Superior Dock

Cabinet: Ore Boat Cabinet

Quest:

```text
Did reported annual shipping tonnage change?
```

Source type:

```text
Duluth Seaway Port Authority Annual Reports, 2005 and 2023 PDFs with CSV appendix
```

Receipt generated:

```text
tonnage summary page pair
```

Art / reward unlocks:

- Ore Boat Marquee Art

## 5. Rochester — Downtown

Cabinet: Heartbeat Cabinet

Quest:

```text
Did the count of commercial building permits change?
```

Source type:

```text
City of Rochester Open Data Portal CSVs, Building Permits 2010 and 2020, addresses redacted, counts only
```

Receipt generated:

```text
filtered count table, no PII
```

Art / reward unlocks:

- Permit Punch Card

## 6. Moorhead — Red River

Cabinet: Gauge Cabinet

Quest:

```text
Did the flood mitigation capital line change?
```

Source type:

```text
City of Moorhead Council Packets, 1997-04-14 and 2009-04-13 PDFs
```

Receipt generated:

```text
Capital Improvement budget line for floodwall, old vs new
```

Art / reward unlocks:

- Flood Gauge Decal

## 7. Bemidji — Paul Bunyan

Cabinet: Axe Cabinet

Quest:

```text
Did county parks spending for the statue area change?
```

Source type:

```text
Beltrami County Annual Financial Audit PDFs, 2008 and 2022, Parks schedule
```

Receipt generated:

```text
expenditure line pair
```

Art / reward unlocks:

- Big Axe Token

## 8. Brainerd — Lakes Country

Cabinet: Bobber Cabinet

Quest:

```text
Did the DNR water-access parking fee change?
```

Source type:

```text
Minnesota DNR State Parks Fee Schedule PDFs, 2000 and 2020
```

Receipt generated:

```text
fee table for public accesses, old vs new
```

Art / reward unlocks:

- Bobber Fee Sticker

## 9. Hibbing — Iron Range

Cabinet: Mine Cart Cabinet

Quest:

```text
Did county-reported mineral lease revenue change?
```

Source type:

```text
St Louis County Auditor Annual Reports, 2012 and 2022 PDFs
```

Receipt generated:

```text
revenue summary line for mineral leases
```

Art / reward unlocks:

- Mine Cart Quarter

## 10. Mankato — River Valley

Cabinet: Corn Cabinet

Quest:

```text
Did the county fairgrounds building rental rate change?
```

Source type:

```text
Blue Earth County Board Packets, 2011-03-22 and 2021-03-23 PDFs, contract appendix
```

Receipt generated:

```text
rental rate page pair
```

Art / reward unlocks:

- Corn Contract Decal

## Travel

Players walk with the joystick.

The loon avatar waddles across the overworld like Link.

Neighboring towns take about 10 seconds.

Longer travel can use the Quarter Line, a pixel light-rail connecting the starter row.

Travel uses Replay tickets, not money.

Later earned cosmetics:

- canoe for lakes
- snowmobile for the north
- bus for the south

Cosmetic only.
No pay-to-win.

## County Unlocks

Counties remain fog until locals clear them.

A county lights up when:

1. any 3 receipts from 3 different towns in that county pass Source Court, and
2. 10 Replay tickets have been spent by players whose home base is in Minnesota

Counties unlock because locals do the work, not because an admin flips a switch.

Governance by Joystick lets locals vote which neighboring county fog lifts next.

## State Unlocks

Minnesota is the tutorial region.

To unlock neighboring state cabinets, a player earns the North Star Badge:

- 50 Source tickets in Minnesota
- 50 Replay tickets in Minnesota
- 50 Context tickets in Minnesota
- at least one Oops Orchid for a correction
- community vote passes with 60 percent yes across the Three Courts

When earned, the Wisconsin, Iowa, North Dakota, and South Dakota cabinets slide into view like a new arcade row.

Players unlock neighbors they can walk to.

They do not unlock all 50 states at once.

## Federal and Global Scale

The map scales by stacking cabinets, not flattening the earth.

### State Row

Each state is one cabinet with 8 to 10 towns inside.

Players only see the state they are in plus neighboring state cabinets.

### Federal Boss Cabinet

Called:

```text
Capitol Arcade
```

It does not show every receipt.

It only shows drifts that passed all Three Courts in five or more states.

Example:

```text
national gas price memory
```

Federal drift plays like a boss level, not a database.

### Global World Fair

Each country is one cabinet.

Art is styled by local players.

Players see the top three memory drifts voted by that country's players, translated to simple cards.

No endless feed.

## Safety Rules

- No fraud declaration. Receipts say only: file A shows X, file B shows Y.
- No authority claim. Courts only check that both files are public and byte-identical.
- No harassment. Starter sources are agencies, not people.
- No PII in public display. If a PDF contains names, the game blurs them behind the membrane and shows only the relevant table.
- Public data is byte-by-byte.
- PII is membrane-restricted.
- Every starter quest is replayable in under 2 minutes by downloading the same two public files from a city, county, state, or agency site.

## Closing Rule

The map stays fun because it grows like an arcade, not like GIS software.

Minnesota starts as a playable world.
Other states become new cabinet rows.
Federal becomes a boss cabinet.
Global becomes a world fair.

Authority remains false.
