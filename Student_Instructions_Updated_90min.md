# Power BI Workshop – Student Instructions (90 Minutes)

© Explore Data Science Academy

## Workshop title
**Visualisation Predict: SDG 1 – Poverty, Unemployment, and COVID-19 in South Africa**

## Workshop goal
In this live 90-minute online workshop, you will use the provided Power BI file to explore the relationship between poverty and unemployment in South Africa across **2017** and **2021**. By the end of the session, you should have a working dashboard, a set of core DAX calculations, and enough evidence to discuss whether the hypothesis is supported by the data.

## Hypothesis
> More South Africans were living in **poverty** in **2021** than in **2017** due to the impact of COVID-19 on **unemployment** rates.

---

# 1. Before the workshop

## What you need installed
Use the **latest version of Power BI Desktop** available to you before the session starts.

Because the Power BI interface changes over time, your layout may look slightly different from screenshots or older recordings. In the latest release, you may notice newer authoring experiences such as:
- updated report authoring controls
- newer visual formatting behaviour
- modern visual defaults and Fluent-style formatting options
- the PBIR report format becoming the default when saving report projects

That is normal. The workshop steps below are written so they still work even if button placement looks slightly different.

## Files you should have ready
- `SDG_1_Student.pbix`
- the supporting data files supplied with the workshop
- this instruction notebook
- the MCQ document for after the build

## Recommended setup
Before the session begins:
1. Open the provided Power BI file.
2. Make sure the data loads without errors.
3. Turn on the **Data**, **Model**, and **Report** views if they are not visible.
4. Save a backup copy of the `.pbix` file before editing.

---

# 2. Dataset context

You are working with two survey-based datasets:
- **NIDS Wave 5 (2017)**
- **NIDS-CRAM Wave 5 (2021)**

These datasets help you compare poverty and employment conditions before and after the strongest COVID-19 disruption period.

## Core tables
### 2017
- `HHRoster_2017`
- `Household_2017`
- `Employment_2017`

### 2021
- `Personal_2021`
- `Household_2021`
- `Employment_2021`

## Important modelling note
There is **no direct relationship** between the 2017 tables and the 2021 tables. To compare both years in interactive visuals, you will need to create small **link tables** such as a province table, year table, or age-band helper table where appropriate.

---

# 3. Learning outcomes

By the end of the workshop, you should be able to:
1. Navigate the latest Power BI Desktop interface confidently.
2. Inspect an existing data model and understand how tables relate to one another.
3. Create calculated columns, calculated tables, and measures using DAX.
4. Build a clean dashboard that compares poverty and employment between 2017 and 2021.
5. Use dashboard evidence to discuss whether the hypothesis is supported.

---

# 4. 90-minute workshop plan

## Segment 1 – Orientation and setup (0 to 10 minutes)
### Objective
Get everyone into the file and aligned on the task.

### What to do
1. Open the provided `.pbix` file.
2. Confirm the tables are loaded.
3. Go to **Model view** and inspect the existing relationships.
4. Identify which tables belong to **2017** and which belong to **2021**.
5. Note that the 2017 data includes a household ID and person ID, while 2021 uses one interviewed individual per household.

### Checkpoint
By minute 10 you should understand:
- what question the dashboard must answer
- which tables you will use most often
- why helper tables are needed for comparisons across years

---

## Segment 2 – Model inspection and helper tables (10 to 25 minutes)
### Objective
Prepare the model so that filtering and comparison are easier.

### Task A: Build a province helper table
Create or import a small province table that contains:
- province name
- province code
- province acronym

Use this table to help standardise province filtering across the 2017 and 2021 datasets.

### Task B: Create a year helper table
Create a small table with:
- `2017`
- `2021`

You can use it later for labelling visuals, creating disconnected logic, or simplifying comparisons.

### Task C: Review relationships
Check the existing relationships and answer these questions:
- Which relationships are `1:*`?
- Which relationships are `1:1`?
- Which relationships use bidirectional filtering?

### Tips for the latest Power BI Desktop
- Relationship editing is still done in **Model view**.
- Some contextual controls may appear in side panes instead of the older ribbon layout.
- If the **on-object** editing experience is enabled, formatting and field assignment may appear directly on the visual.

### Checkpoint
By minute 25 you should have:
- a clear view of the model
- province support ready
- confidence moving between Report, Data, and Model views

---

## Segment 3 – Create core DAX features (25 to 50 minutes)
### Objective
Create the fields needed for analysis.

Build the following in order.

## 3.1 Age features
Create age or age-band logic for both years so that you can compare groups such as:
- under 18
- 18 to 24
- 25 to 34
- 35 to 54
- 55 to 64
- 65+

Keep the grouping consistent across both years.

## 3.2 Poverty features
Create fields that classify households or individuals into the required poverty categories:
- **FPL** – Food Poverty Line
- **LBPL** – Lower Bound Poverty Line
- **UBPL** – Upper Bound Poverty Line
- **None**

Also create measures for:
- percentage under each poverty level
- total people or households in each category

## 3.3 Employment features
Create employment status categories that clearly separate:
- employed
- self-employed
- unemployed
- not economically active

Then create measures for:
- Labour Force Participation Rate
- unemployment rate
- employment distribution by province and age group

## 3.4 Basic comparison measures
Create measures that let you compare 2017 and 2021, for example:
- mean age by province and year
- poverty percentage by province and year
- GNI per capita by province and year
- employed plus self-employed share

### Best practice reminders
- Use **measures** for calculations that should respond to filters.
- Use **calculated columns** when a row-level classification is needed.
- Name measures clearly, for example: `Poverty % 2021`, `Mean Age 2017`, `LFPR 2021`.
- Format percentages as percentages and currency as rand values.

### Checkpoint
By minute 50 you should have the core fields needed for visuals.

---

## Segment 4 – Build the dashboard (50 to 75 minutes)
### Objective
Turn the model into a clear visual story.

Build **one dashboard page** that answers the hypothesis.

## Minimum visual requirements
Include at least:
1. **A title section** with the dashboard purpose.
2. **A province visual** such as a map or filled map if available.
3. **A poverty comparison visual** between 2017 and 2021.
4. **An employment comparison visual** between 2017 and 2021.
5. **An age-related visual** showing how age groups compare.
6. **At least one KPI/card** with a headline number.
7. **A slicer area** for province, year, and employment status where relevant.

## Suggested visual layout
### Left side
- province slicer
- year slicer if useful
- summary cards

### Centre
- poverty comparison visual
- unemployment or LFPR visual

### Right side
- age group visual
- GNI or province comparison visual

## Visual design rules
- Keep colours consistent across years.
- Label visuals clearly.
- Avoid clutter.
- Do not use too many chart types on one page.
- Make sure visuals are interactive where comparison makes sense.

## Latest Power BI note
In newer versions of Power BI Desktop, visual building may happen either through:
- the traditional **Build visual / Format visual** panes, or
- direct **on-object interaction** on the canvas

Either approach is fine. Use whichever is available in your version.

### Checkpoint
By minute 75 you should have a clean, usable dashboard.

---

## Segment 5 – Interpretation, MCQs, and wrap-up (75 to 90 minutes)
### Objective
Use the dashboard to answer questions and prepare for discussion.

## Final analysis task
Use your dashboard to answer:
1. Did poverty increase from 2017 to 2021?
2. How did unemployment change?
3. Which provinces stand out most?
4. Which age groups appear most affected?
5. Does the evidence support the hypothesis fully, partly, or not at all?

## MCQ preparation
After building the dashboard, complete the MCQ activity. Your dashboard should help you answer the visual interpretation questions.

## Short presentation prompt
Prepare a **2 to 3 minute verbal summary** covering:
- what you built
- what your main findings are
- whether the hypothesis is supported
- one limitation of the data

---

# 5. What you should submit after the workshop

## Required deliverables
1. Your updated **Power BI dashboard** file.
2. Completed **MCQ answers**.
3. A short summary of findings.

## Recommended summary structure
- **Hypothesis:** state whether you support it or not.
- **Evidence:** mention 2 to 4 dashboard findings.
- **Insight:** explain what changed between 2017 and 2021.
- **Limitation:** mention one survey or sampling limitation.

---

# 6. Practical Power BI guidance for the latest desktop version

## If the interface looks different
Do not panic. In the newest Power BI Desktop releases, these are the main things to remember:
- **Model view** is still where relationships are checked and edited.
- **Data view** is still where you inspect row-level values.
- **Report view** is where visuals are built.
- Measures, columns, and tables can still be created from the modelling tools or contextual menus.
- Formatting may appear in a side pane or directly on the visual, depending on whether on-object interaction is enabled.

## If a visual option is hard to find
Try one of these:
1. Right-click the table or field.
2. Use the top search bar in Power BI.
3. Open the contextual visual menu on the canvas.
4. Check whether your organisation has preview features turned on.

## Save often
Because Power BI can be resource-heavy, save your work after each major step.

---

# 7. Success checklist

Before the workshop ends, make sure you can say yes to these:
- I understand the hypothesis.
- I can explain the difference between the 2017 and 2021 datasets.
- I created the main DAX fields needed for analysis.
- I built an interactive dashboard page.
- I can use the dashboard to defend a conclusion.

---

# 8. Closing note

The aim of this workshop is not just to make charts. It is to use Power BI to turn raw survey data into a defensible story about poverty, unemployment, and the social effects of COVID-19 in South Africa.
