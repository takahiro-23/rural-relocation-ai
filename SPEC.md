Calendar Apartment App (MVP) Specification
==========================================

Overview
--------
This is a calendar app that presents a monthly view as a modern apartment facade.
Each day is a door. Tapping a door opens a single-room interior for that date.
Events appear as physical objects inside the room, so users can recognize schedules
at a glance.

Platform
--------
- Flutter (iOS + Android)

Core User Flow
--------------
- Launch app -> month facade (5x7 grid, always month view)
- Tap a door -> room view for that date
- Add event -> object appears in the room
- Tap object -> speech bubble with details (title/time/memo)

Month View (Apartment Facade)
-----------------------------
- Grid: 5x7 calendar layout, Sunday start by default
- Week start toggle in settings (Sunday/Monday)
- Day numbers are large and centered on each door
- Days with events show a small marker (e.g., light or mailbox)
- Month navigation with left/right arrows
- Always month view; no week-only mode

Room View (Single Room)
-----------------------
- Date label at top
- Room area: 6x4 grid (24 slots total)
- Objects are size 1 slot, no scaling
- Drag and drop placement
- No overlap; objects snap to nearest free slot
- Depth layers: 3 levels (front/middle/back)
- Render order: depth -> y

Events and Objects
------------------
- Each event is linked to one object type
- Multiple events per day create multiple objects
- Empty day shows an empty room
- Object tap shows bubble with title/time/memo and edit/delete

Initial Categories (20)
-----------------------
- Birthday: cake, balloons
- Anniversary: flowers, wine
- Study: desk, textbooks
- Exam: good-luck charm, wall notes
- Work: laptop, paperwork
- Meeting: whiteboard, small chair
- Exercise: yoga mat, dumbbell
- Clinic: medicine bag, medical card
- Travel: suitcase, map
- Shopping: paper bag
- Friends: coffee cup, two chairs
- Date: candles, flowers
- Cooking: frying pan, ingredients
- Cleaning: vacuum
- Payment/Bill: invoice, envelope
- Class/Lecture: notebook, pen
- Move/Organize: boxes
- Hobby/Creative: paintbrush, canvas
- Movie/Event: ticket, popcorn
- Family: photo frame, small toy

Time of Day and Weather
-----------------------
- Time zones (local time):
  - Day: 08:00-16:59
  - Evening: 17:00-18:59
  - Night: 19:00-05:59
  - Morning: 06:00-07:59
- Weather types: clear, cloudy, rain, snow (same intensity)
- Night: door lights on
- Weather source: location + weather API (e.g., OpenWeather)

Monetization (IAP)
------------------
- Free: 20 categories and standard apartment theme
- IAP (one-time):
  - Apartment exterior skins
  - Room themes (wall/floor)
  - Furniture/decoration packs
  - Seasonal themes

Data Model (MVP)
----------------
- CalendarSettings: week_start ("sun" | "mon")
- Category: id, name, icon_id, default_item_type_ids
- ItemType: id, name, asset_id, size_slots (=1)
- Event: id, date, title, time?, memo?, category_id, item_type_id
- RoomPlacement: id, event_id, date, slot_index (0-23), depth (0|1|2)

Next Steps
----------
- Initialize Flutter project
- Implement month view layout with 5x7 door grid
- Implement room view with 6x4 grid and drag placement
